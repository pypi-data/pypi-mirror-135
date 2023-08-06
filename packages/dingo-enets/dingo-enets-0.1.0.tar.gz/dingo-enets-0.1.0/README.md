# dingo-enets
This reposity contains the embedding networks from [1], which are trained for the purpose of gravitational wave parameter estimation. If you find this code useful please cite [1].

Note: This is only a partial release of the code used in [1]. A more comprehensive package will be released in the near future. The present repository will not be maintained once the full package is publicly available.

## Usage

Build a virtual environment and install `dingo-enets`.
```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install dingo-enets
```

Use `dingo-enets` to download and build a trained embedding network for a particular observing run. The model will be saved in `</path/to/model_directory>`.
```python
> from dingo_enets import build_enet
> enet = build_enet(run="O1", detectors=["H1", "L1"], model_dir="</path/to/model_directory>")

> import torch
> input = torch.rand(10, 2, 3, 8033)
> output = enet(input)
> print(output.shape)
```
The function `build_enet` recognises whether a suitable model is present in the model directory, in which case it is not downloaded but instead loaded directly from disk. 

## References
[1] M. Dax, S.R. Green, J. Gair, J.H. Macke, A. Buonanno, B. Schölkops, _Real-Time Gravitational Wave Science with Neural Posterior Estimation_, Phys.Rev.Lett. 127 (2021) 24, 241103.
[[arXiv]](https://arxiv.org/abs/2106.12594) [[inspirehep]](https://inspirehep.net/literature/1870159)

