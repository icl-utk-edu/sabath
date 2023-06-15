# SABATH: Surrogate AI Benchmarking Applications' Testing Harness

SABATH provides benchmarking infrastructure for evaluating scientific ML/AI
models. It contains support for scientific machine learning surrogates from
external repositories such as
[SciML-Bench](https://github.com/stfc-sciml/sciml-bench).


The software dependences are explicitly exposed in the surrogate model
definition, which allows the use of advanced optimization, communication, and
hardware features.  For example,  distributed, multi-GPU training may be
enabled with [Horovod](https://github.com/horovod/horovod). Surrogate models
may be implemented using [TensorFlow](https://www.tensorflow.org/),
[PyTorch](https://pytorch.org/), or [MXNET](https://mxnet.apache.org/)
frameworks.

## Installing Prerequisites

Models controlled by SABATH have a number of software prerequisites that can be
satisfied with different methods described below.

### Using Anaconda or Conda version 3 for Installing Prerequisites

1. Setup the shell environment with a path for the Anaconda/Conda 3
   installation as well as both SABATH's repo location and Python 3
   interpreter with prerequisite modules installed. Type in bash or zsh shells:

```sh
export CONDA_PREFIX=/path/to/conda3
export SABATH_ROOT=/path/to/sabath
export SABATH_PYTHON=$CONDA_PREFIX/bin/python3
```

Note that the standard shell environment variables such as `PATH` are not
modified as to not interfere with the environment activation performed by
Anaconda/Conda (see below).

2. Download Anaconda 3 (version 2022.9 for Linux with Python version 3.9),
   which has a size of over 700 MB. Type:

```sh
wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh
```

or Conda 3 (version 23.3.1 for Linux with Python version 3.8), which has a size
of almost 70 MB:

```sh
wget https://repo.anaconda.com/miniconda/Miniconda3-py38_23.3.1-0-Linux-x86_64.sh
```

3. Install Anaconda 3 (`-b` option switches the installation to batch mode
   which requires no user input but implicitly accepts the Anacondaa license
   terms) by typing:

```sh
bash Anaconda3-2022.10-Linux-x86_64.sh -b -p $CONDA_PREFIX
```

or install Conda 3 (the flags are the same as for Anaconda 3, shown above):

```sh
bash Miniconda3-py38_23.3.1-0-Linux-x86_64.sh -b -p $CONDA_PREFIX
```

4. Initialize Anaconda/Conda 3 in manner specific for the shell of your choice
   and restart the shell for the changes take effect in future shells. For
   the bash shell, type:

```sh
$CONDA_PREFIX/bin/conda init bash ; exec bash
```

 For the zsh shell, type:

```sh
$CONDA_PREFIX/bin/conda init zsh ; exec zsh
```

The proper initialization for other shells is also available.  After
initialization, `conda` will be available as a regular command because the
`PATH` environment variable is modified.

5. Create an Anaconda/Conda 3 environment for SABATH using the SABATH's
   provided environment file that forces a download of the direct prerequisites
   and their dependencies. Type:

```sh
conda env create -f $SABATH_ROOT/etc/conda3/environment.yml
```

The command might take a while as the solver from Anaconda/Conda 3 computes the
transitive set of dependencies and downloads them in turn. The sample output
will show the subsequent stages of the process:

```log
Collecting package metadata (repodata.json): ...working... done
Solving environment: ...working...
```

Depending on your operating system, the size of the downloaded files might
exceed 7 GB.

5. Activate the Anaconda/Conda 3 environment for use by SABATH by typing:

```sh
conda activate sabath
```

6. To deactivate the Anaconda/Conda 3 environment used by SABATH by typing:

```sh
conda deactivate sabath
```

Note that the Anaconda/Conda 3 environment has to remain activated to use
SABATH, its models,  and their dependencies.

7. To remove the Anaconda/Conda 3 environment used by SABATH by typing:

```sh
conda env remove -n sabath
```

Note that some of the downloaded files will still be cache inside your
Anaconda/Conda 3 directory.

8. It is possible to undo changes for your shell's dot-files. For bash, type:

```sh
conda init --reverse -n sabath bash ; exec bash
```

And for zsh, type:

```sh
conda init --reverse -n sabath zsh ; exec zsh
```
