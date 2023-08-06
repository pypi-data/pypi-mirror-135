import numpy as np


def lukasiewicz_strict_ordering_factory(r):
    def strict_ordering(x, y):
        return min(1, max(0, 1 / r * (y - x)))

    return strict_ordering


def product_strict_ordering_factory(r):
    def strict_ordering(x, y):

        return max(0, 1 - np.exp(-1 * 1 / r * (y - x)))

    return strict_ordering


def classic_ordering(x, y):
    return x < y
