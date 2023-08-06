# Zeef: Interactive Learning for Python

![PyPI](https://img.shields.io/pypi/v/zeef?color=green) [![Downloads](https://pepy.tech/badge/zeef)](https://pepy.tech/project/zeef) [![Testing](https://github.com/MLSysOps/zeef/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/MLSysOps/zeef/actions/workflows/main.yml) [![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2FMLSysOps%2Fdeepal.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2FMLSysOps%2Fdeepal?ref=badge_shield)

An interactive learning framework for data-centric AI.

![](./docs/images/logo.svg)

Zeef is featured for

- **Active learning** - Off the shelf data selection algorithms to reduce the labor of data annotation.
- **Continual learning** - Easy to use APIs to prototype a continual learning workflow instantly.

## Installation

```shell
pip install zeef
```

For the local development, you can install from the [Anaconda](https://www.anaconda.com/) environment by

```shell
conda env create -f environment.yml
```

## Quick Start

We can start from the easiest example: random select data points from an unlabeled data pool.

```python
from sklearn import svm

from zeef.data import Pool
from zeef.learner.sklearn import Learner
from zeef.strategy import RandomSampling

data_pool = Pool(unlabeled_data)  # generate the data pool.
# define the sampling strategy and the SVM learner.
strategy = RandomSampling(data_pool, learner=Learner(net=svm.SVC(probability=True)))

query_ids = strategy.query(1000)  # query 1k samples for labeling.
data_pool.label_by_ids(query_ids, data_labels)  # label the 1k samples.
strategy.learn()  # train the model using all the labeled data.
strategy.infer(test_data)  # evaluate the model.
```

A quick MNIST CNN example can be found in [here](examples/mnist/torch_al.py). Run

```shell
python torch_al.py
```

to start the quick demonstration.

## License

[Apache License 2.0](./LICENSE)
