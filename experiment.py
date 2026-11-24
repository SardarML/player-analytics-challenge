from math import sqrt

from scipy.stats import norm


def two_proportion_test(x1, x2, n, alpha=0.05, power=0.8):
    """Return the two-sided p-value and the sample size per group for equal groups of size n."""
    p1, p2 = x1 / n, x2 / n
    pooled = (p1 + p2) / 2
    z = (p2 - p1) / sqrt(pooled * (1 - pooled) * 2 / n)
    variance = p1 * (1 - p1) + p2 * (1 - p2)
    z_total = norm.ppf(1 - alpha / 2) + norm.ppf(power)
    return 2 * norm.sf(abs(z)), z_total ** 2 * variance / (p2 - p1) ** 2
