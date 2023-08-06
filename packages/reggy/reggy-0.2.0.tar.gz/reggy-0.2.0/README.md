# reggy

[![PyPI](https://img.shields.io/pypi/v/reggy.svg?style=flat)](https://pypi.python.org/pypi/reggy)
[![Tests](https://github.com/kpj/reggy/workflows/Tests/badge.svg)](https://github.com/kpj/reggy/actions)

Python package for regularized regressions.

Supported regularization terms:
* Ridge
* LASSO
* Network-fusion penalty (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6030897/)


## Installation

```bash
$ pip install reggy
```


## Usage

A simple example with LASSO regularization:
```python
import reggy
import numpy as np


alpha = 0.3
beta = 1.7

X = np.random.normal(size=(100, 1))
y = np.random.normal(X * beta + alpha, size=(100, 1))

model = reggy.RegReg(X, y, family=reggy.gaussian_family, regularizers=[(0.5, reggy.lasso)])
model.fit()

print(model.intercept_, model.coef_)
## [[0.22491232]] [[0.9219889]]
```
