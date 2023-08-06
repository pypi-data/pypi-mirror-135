from typing import Tuple, Callable, Union
import numpy as np
import torch
import torch.nn as nn
from torch.nn import functional as F
from nflows.nn.nets.resnet import ResidualBlock


class LinearProjectionRB(nn.Module):
    """
    A compression layer that reduces the input dimensionality via projection
    onto a reduced basis. The input data is of shape (batch_size, num_blocks,
    num_channels, num_bins). Each of the num_blocks blocks (for GW use case:
    block=detector) is treated independently.

    A single block consists of 1D data with num_bins bins (e.g. GW use case:
    num_bins=number of frequency bins). It has num_channels>=2 different
    channels, channel 0 and 1 store the real and imaginary part of the
    signal. Channels with index >=2 are used for auxiliary signals (such as
    PSD for GW use case).

    This layer compresses the complex signal in channels 0 and 1 to n_rb
    reduced-basis (rb) components. This is achieved by initializing the
    weights of this layer with the rb matrix V, such that the (2*n_rb)
    dimensional output of each block is the concatenation of the real and
    imaginary part of the reduced basis projection of the complex signal in
    channel 0 and 1. The projection of the auxiliary channels with index >=2
    onto these components is initialized with 0.

    Module specs
    ----------
        input dimension:    (batch_size, num_blocks, num_channels, num_bins)
        output dimension:   (batch_size, 2 * n_rb * num_blocks)
    """

    def __init__(
        self,
        input_dims: Tuple[int, int, int],
        n_rb: int,
        V_rb_list: Union[Tuple, None] = None,
    ):
        """
        Parameters
        ----------
        input_dims : tuple
            dimensions of input batch, omitting batch dimension
            input_dims = (num_blocks, num_channels, num_bins)
        n_rb : int
            number of reduced basis elements used for projection
            the output dimension of the layer is 2 * n_rb * num_blocks
        V_rb_list : tuple of np.arrays, or None
            tuple with V matrices of the reduced basis SVD projection,
            convention for SVD matrix decomposition: U @ s @ V^h;
            if None, layer is not initialized with reduced basis projection,
            this is useful when loading a saved model
        """

        super(LinearProjectionRB, self).__init__()

        self.input_dims = input_dims
        self.num_blocks, self.num_channels, self.num_bins = self.input_dims
        self.n_rb = n_rb

        # define a linear projection layer for each block
        layers = []
        for _ in range(self.num_blocks):
            layers.append(nn.Linear(self.num_bins * self.num_channels, self.n_rb * 2))
        self.layers = nn.ModuleList(layers)

        # initialize layers with reduced basis
        if V_rb_list is not None:
            self.test_dimensions(V_rb_list)
            self.init_layers(V_rb_list)

    @property
    def input_dim(self):
        return self.num_bins * self.num_channels * self.num_blocks

    @property
    def output_dim(self):
        return 2 * self.n_rb * self.num_blocks

    def test_dimensions(self, V_rb_list):
        """Test if input dimensions to this layer are consistent with each
        other, and the reduced basis matrices V."""
        if self.num_channels < 2:
            raise ValueError(
                "Number of channels needs to be >=2, for real and imaginary parts."
            )
        if len(V_rb_list) != self.num_blocks:
            raise ValueError(
                "There must be exactly one reduced basis matrix V for each block."
            )
        for V in V_rb_list:
            if not isinstance(V, np.ndarray) or len(V.shape) != 2:
                raise ValueError(
                    "Reduced basis matrix V must be a numpy array with 2 axes."
                )
            if V.shape[0] != self.num_bins:
                raise ValueError(
                    "Number of input bins needs to match number of rows in rb matrix V."
                )
            if V.shape[1] < self.n_rb:
                raise ValueError(
                    "More reduced basis elements requested than available."
                )

    def init_layers(self, V_rb_list):
        """
        Loop through layers and initialize them individually with the
        corresponding rb projection. V_rb_list is a list that contains the rb
        matrix V for each block. Each matrix V in V_rb_list is represented
        with a numpy array of shape (self.num_bins, num_el), where
        num_el >= self.n_rb.

        Parameters
        ----------
        V_rb_list : tuple of np.arrays
            tuple with V matrices of the reduced basis SVD projection,
            convention for SVD matrix decomposition: U @ s @ V^h
        """
        n = self.n_rb
        k = self.num_bins
        for ind, layer in enumerate(self.layers):
            V = V_rb_list[ind]

            # truncate V to n_rb basis elements
            V = V[:, :n]
            V_real = torch.from_numpy(V.real).float()
            V_imag = torch.from_numpy(V.imag).float()

            # initialize all weights and biases with zero
            layer.weight.data = torch.zeros_like(layer.weight.data)
            layer.bias.data = torch.zeros_like(layer.bias.data)

            # load matrix V into weights
            layer.weight.data[:n, :k] = torch.transpose(V_real, 1, 0)
            layer.weight.data[n:, :k] = torch.transpose(V_imag, 1, 0)
            layer.weight.data[:n, k : 2 * k] = -torch.transpose(V_imag, 1, 0)
            layer.weight.data[n:, k : 2 * k] = torch.transpose(V_real, 1, 0)

    def forward(self, x):
        if x.shape[1:] != (self.num_blocks, self.num_channels, self.num_bins):
            raise ValueError("Invalid shape for projection layer.")
        out = []
        for ind in range(self.num_blocks):
            out.append(self.layers[ind](x[:, ind, ...].flatten(start_dim=1)))
        x = torch.cat(out, dim=1)
        return x


class DenseResidualNet(nn.Module):
    """
    A nn.Module consisting of a sequence of dense residual blocks. This is
    used to embed high dimensional input to a compressed output. Linear
    resizing layers are used for resizing the input and output to match the
    first and last hidden dimension, respectively.

    Module specs
    --------
        input dimension:    (batch_size, input_dim)
        output dimension:   (batch_size, output_dim)
    """

    def __init__(
        self,
        input_dim: int,
        output_dim: int,
        hidden_dims: Tuple,
        activation: Callable = F.elu,
        dropout: float = 0.0,
        batch_norm: bool = True,
    ):
        """
        Parameters
        ----------
        input_dim : int
            dimension of the input to this module
        output_dim : int
            output dimension of this module
        hidden_dims : tuple
            tuple with dimensions of hidden layers of this module
        activation: callable
            activation function used in residual blocks
        dropout: float
            dropout probability for residual blocks used for reqularization
        batch_norm: bool
            flag that specifies whether to use batch normalization
        """

        super(DenseResidualNet, self).__init__()
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.hidden_dims = hidden_dims
        self.num_res_blocks = len(self.hidden_dims)

        self.initial_layer = nn.Linear(self.input_dim, hidden_dims[0])
        self.blocks = nn.ModuleList(
            [
                ResidualBlock(
                    features=self.hidden_dims[n],
                    context_features=None,
                    activation=activation,
                    dropout_probability=dropout,
                    use_batch_norm=batch_norm,
                )
                for n in range(self.num_res_blocks)
            ]
        )
        self.resize_layers = nn.ModuleList(
            [
                nn.Linear(self.hidden_dims[n - 1], self.hidden_dims[n])
                if self.hidden_dims[n - 1] != self.hidden_dims[n]
                else nn.Identity()
                for n in range(1, self.num_res_blocks)
            ]
            + [nn.Linear(self.hidden_dims[-1], self.output_dim)]
        )

    def forward(self, x):
        x = self.initial_layer(x)
        for block, resize_layer in zip(self.blocks, self.resize_layers):
            x = block(x, context=None)
            x = resize_layer(x)
        return x


def create_enet_with_projection_layer_and_dense_resnet(
    input_dims: Tuple[int, int, int],
    n_rb: int,
    output_dim: int,
    hidden_dims: Tuple,
    V_rb_list: Union[Tuple, None] = None,
    dropout: float = 0.0,
    batch_norm: bool = True,
):
    """
    Builder function for 2-stage embedding network for 1D data with multiple
    blocks and channels. Module 1 is a linear layer initialized as the
    projection of the complex signal onto reduced basis components via the
    LinearProjectionRB, where the blocks are kept separate. See docstring
    of LinearProjectionRB for details. Module 2 is a sequence of dense residual
    layers, that is used to further reduce the dimensionality.

    The projection requires the complex signal to be represented via the real
    part in channel 0 and the imaginary part in channel 1. Auxiliary signals
    may be contained in channels with indices => 2. In GW use case a block
    corresponds to a detector and channel 2 is used for ASD information.

    Module specs
    ----------
    input dimension:    (batch_size, num_blocks, num_channels, num_bins)
    output dimension:   (batch_size, output_dim)

    Parameters
    ----------
    input_dims: tuple
        dimensions of input batch, omitting batch dimension
        input_dims = (num_blocks, num_channels, num_bins)
    n_rb: int
        number of reduced basis elements used for projection
        the output dimension of the layer is 2 * n_rb * num_blocks
    output_dim: int
        output dimension of the full module
    hidden_dims: tuple
        tuple with dimensions of hidden layers of module 2
    V_rb_list: tuple of np.arrays, or None
        tuple with V matrices of the reduced basis SVD projection,
        convention for SVD matrix decomposition: U @ s @ V^h;
        if None, layer is not initialized with reduced basis projection,
        this is useful when loading a saved model
    dropout: float
        dropout probability for residual blocks used for reqularization
    batch_norm: bool
        flag that specifies whether to use batch normalization

    Returns
    ----------
    enet: nn.Module
        embedding network
    """
    module_1 = LinearProjectionRB(input_dims, n_rb, V_rb_list)
    module_2 = DenseResidualNet(
        input_dim=module_1.output_dim,
        output_dim=output_dim,
        hidden_dims=hidden_dims,
        activation=F.elu,
        dropout=dropout,
        batch_norm=batch_norm,
    )
    enet = nn.Sequential(module_1, module_2)
    return enet
