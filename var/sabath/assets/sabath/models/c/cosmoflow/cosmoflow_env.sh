#!/bin/bash --login

set -exo pipefail


export CUDA_HOME=$CONDA_PREFIX/bin/
export PATH=$CUDA_HOME:$PATH
export LD_LIBRARY_PATH=$CONDA_PREFIX:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib64:$LD_LIBRARY_PATH


# set relevant build variables for Horovod
export HOROVOD_CUDA_HOME=$CUDA_HOME
export HOROVOD_NCCL_HOME=$CONDA_PREFIX
export HOROVOD_GPU_OPERATIONS=NCCL

pip install -r requirements.txt
