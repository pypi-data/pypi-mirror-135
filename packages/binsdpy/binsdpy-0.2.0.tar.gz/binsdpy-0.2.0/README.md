[![build](https://github.com/mikulatomas/binsdpy/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/mikulatomas/binsdpy/actions/workflows/build.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/mikulatomas/binsdpy/branch/main/graph/badge.svg?token=HI1I1OVOXK)](https://codecov.io/gh/mikulatomas/binsdpy)
[![PyPI version](https://badge.fury.io/py/binsdpy.svg)](https://badge.fury.io/py/binsdpy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# binsdpy - binary similarity and distance measures
Python implementation of binary similarity (see [1]) and distance measures (see [2]). The `bitsets` (immutable ordered set data type) and `numpy.ndarray` are suported as feature vectors.

## Example
Example based on `bitsets`:
```python
from bitsets import bitset
from binsdpy.similarity import jaccard
from binsdpy.distance import euclid

Colors = bitset("Colors", ("red", "blue", "green", "yellow"))

a = Colors.frommembers(["red", "blue"])
b = Colors.frommembers(["red", "yellow"])

jaccard(a, b)
# > 0.3333333333333333
euclid(a, b)
# > 1.4142135623730951
```

Example based on `np.ndarray`:
```python
import numpy as np
from binsdpy.similarity import jaccard
from binsdpy.distance import euclid

a = np.array([1, 1, 0, 0], dtype=bool)
b = np.array([1, 0, 0, 1], dtype=bool)

jaccard(a, b)
# > 0.3333333333333333
euclid(a, b)
# > 1.4142135623730951
```

## Installation
Package is avaliable in alpha version via `pip`.

```bash
$ pip install binsdpy
```

## Dependencies
binsdpy requires:

* Python (>= 3.6)
* bitset
* numpy

## Reference
> [1] Brusco, M., Cradit, J. D., & Steinley, D. (2021). A comparison of 71 binary similarity coefficients: The effect of base rates. Plos one, 16(4), e0247751.
https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0247751
> [2] Choi, S. S., Cha, S. H., & Tappert, C. C. (2010). A survey of binary similarity and distance measures. Journal of systemics, cybernetics and informatics, 8(1), 43-48.
http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.352.6123&rep=rep1&type=pdf

