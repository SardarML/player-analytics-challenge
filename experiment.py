from math import sqrt

from scipy.stats import norm


def two_proportion_test(x1, x2, n, alpha=0.05, power=0.80):
    """Return the two-sided p-value and required players per group (equal group sizes)."""
    p1, p2 = x1 / n, x2 / n
    pooled = (p1 + p2) / 2
    z = (p2 - p1) / sqrt(pooled * (1 - pooled) * 2 / n)
    variance = p1 * (1 - p1) + p2 * (1 - p2)
    needed = (norm.ppf(1 - alpha / 2) + norm.ppf(power)) ** 2 * variance / (p2 - p1) ** 2
    return {"p_value": 2 * norm.sf(abs(z)), "players_per_group": needed}
