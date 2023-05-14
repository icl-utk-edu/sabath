# SABATH: Surrogate AI Benchmarking Applications' Testing Harness

SABATH provides benchmarking infrastructure for evaluating scientific ML/AI
models. It contains support for scientific machine learning surrogates from
external repositories such as
[SciML-Bench](https://github.com/stfc-sciml/sciml-bench.git)).

The software dependences are explicitly exposed in the surrogate model
definition, which allows the use of advanced optimization, communication, and
hardware features.  For example,  distributed, multi-GPU training may be
enabled with [Horovod](https://github.com/horovod/horovod). Surrogate models
may be implemented using [TensorFlow](https://www.tensorflow.org/),
[PyTorch](https://pytorch.org/), or [MXNET](https://mxnet.apache.org/)
frameworks.
