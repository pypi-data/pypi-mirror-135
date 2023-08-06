[![PyPI version](https://badge.fury.io/py/fuzzycorr.svg)](https://badge.fury.io/py/fuzzycorr)
[![codecov](https://codecov.io/gh/mikulatomas/fuzzycorr/branch/main/graph/badge.svg?token=LRLWZI58ID)](https://codecov.io/gh/mikulatomas/fuzzycorr)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# fuzzycorr
A ``numpy`` implementation of Robust Rank Correlation Coefficients (fuzzy correlation) based on paper:

```
Bodenhofer, U., and F. Klawonn. "Robust rank correlation coefficients on the basis of fuzzy."
Mathware & Soft Computing 15.1 (2008): 5-20.
```

This implementation is experimental and need future optimization and testing.

## Installation

This package will be avaliable soon on ``pip``.

## Basic usage

```python
from fuzzycorr import fuzzy_correlation_factory
from fuzzycorr.strict_orderings import lukasiewicz_strict_ordering_factory
from fuzzycorr.t_norms import godel

# create strict fuzzy ordering or supply own one
strict_ordering = lukasiewicz_strict_ordering_factory(r=0.2)

# create fuzzy correlation function with tnorm
fuzzy_corr = fuzzy_correlation_factory(strict_ordering, godel)

# load data
x = np.random.random(10)
y = np.random.random(10)

# calculate fuzzy correlation
fuzzy_corr(x, y)
```

Visit [example Jupiter Notebook](example.ipynb).