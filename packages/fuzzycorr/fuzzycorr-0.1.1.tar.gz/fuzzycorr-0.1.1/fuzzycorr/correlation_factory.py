import numpy as np
from fuzzycorr.utils import permutation_pairs


def fuzzy_correlation_factory(strict_ordering, t_norm):
    """Meta function for creating fuzzy correlation function"""

    vstrict_ordering = np.vectorize(strict_ordering, otypes=[np.float64])
    vt_norm = np.vectorize(t_norm, otypes=[np.float64])

    def fuzzy_correlation(x, y):
        input_len = x.shape[0]
        index_permutations = permutation_pairs(np.arange(input_len))

        xi, xj = x[index_permutations].T
        yi, yj = y[index_permutations].T

        xixj = vstrict_ordering(xi, xj)
        yiyj = vstrict_ordering(yi, yj)
        yjyi = vstrict_ordering(yj, yi)

        concordant_pairs = vt_norm(xixj, yiyj)
        discordant_pairs = vt_norm(xixj, yjyi)

        c = np.sum(concordant_pairs)

        d = np.sum(discordant_pairs)

        return (c - d) / (c + d)

    return fuzzy_correlation
