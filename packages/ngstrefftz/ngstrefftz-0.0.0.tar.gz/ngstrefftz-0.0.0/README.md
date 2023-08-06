# NGSTrefftz
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/PaulSt/NGSTrefftz/HEAD?filepath=notebooks%2Findex.ipynb)
[![Docker Image Version (latest by date)](https://img.shields.io/docker/v/paulstdocker/ngstrefftz?label=docker&logo=docker)](https://hub.docker.com/repository/docker/paulstdocker/ngstrefftz)
[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/PaulSt/NGSTrefftz/build?logo=github)](https://github.com/PaulSt/NGSTrefftz/actions)

Trefftz and quasi-Trefftz functions for the acoustic wave equation implemented for NGSolve.

## Try it out!
* Launch the Binder here:   
  [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/PaulSt/NGSTrefftz/HEAD?filepath=notebooks%2Findex.ipynb)
* Or run the docker locally (you need to have docker installed):
```bash
git clone https://github.com/PaulSt/NGSTrefftz
cd NGSTrefftz && docker build -t ngstrefftz_jupyter .
docker run -p 8888:8888 ngstrefftz_jupyter
```

## Installing from source
You need to have ![ngsolve](https://ngsolve.com/) installed.
```bash
git clone --recursive https://github.com/PaulSt/NGSTrefftz
mkdir ./NGSTrefftz/make && cd ./NGSTrefftz/make
cmake ../src && make install
```
For tent-pitching the code uses ![ngstents](https://github.com/jayggg/ngstents).

## Papers using the code
* Tent pitching and Trefftz-DG method for the acoustic wave equation  
[![arXiv](https://img.shields.io/badge/arXiv-1907.02367-b31b1b.svg)](https://arxiv.org/abs/1907.02367)
* A space-time quasi-Trefftz DG method for the wave equation with piecewise-smooth coefficients  
[![arXiv](https://img.shields.io/badge/arXiv-2011.04617-b31b1b.svg)](https://arxiv.org/abs/2011.04617)
* Embedded Trefftz discontinuous Galerkin methods  
[![arXiv](https://img.shields.io/badge/arXiv-2201.07041-b31b1b.svg)](https://arxiv.org/abs/2201.07041)


![](.github/wave.gif)

