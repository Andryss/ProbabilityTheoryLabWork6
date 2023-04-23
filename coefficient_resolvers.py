from scipy.stats import chi2, t, norm


def normal_distribution_function_coefficient_resolver(result: float) -> float:
    return norm.ppf(result)


def student_distribution_coefficient_resolver(n: int, p: float) -> float:
    return t.ppf(p, n)


def pearson_distribution_coefficient_resolver(n: int, p: float) -> float:
    return chi2.ppf(p, n)
