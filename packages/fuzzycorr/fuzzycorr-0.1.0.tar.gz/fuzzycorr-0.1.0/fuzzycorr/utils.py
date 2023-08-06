import numpy as np


def permutation_pairs(x):
    """Fast way how calculate all permutations suggested by @Jaime on 
    https://stackoverflow.com/questions/27323448/numpy-array-to-permutation-matrix.

    There is probably still room for improvement."""

    n = x.shape[0]
    perm = np.empty((n, n, 2), dtype=x.dtype)
    perm[..., 0] = x[:, None]
    perm[..., 1] = x
    perm = perm.reshape(-1, 2)

    return np.delete(perm, np.arange(0, perm.shape[0], n + 1), axis=0)
