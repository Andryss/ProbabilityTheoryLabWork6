
_normal_distribution_function_values: dict[float, float] = {
    0.5000: 0.0, 0.5040: 0.01
    # ...
}


def normal_distribution_function_coefficient_resolver(result: float) -> float:
    assert 0.5 <= result < 1, "Result must be in range [0.5; 1)"
    if result not in _normal_distribution_function_values:
        raise Exception(f"Normal distribution coefficient for value {result} hasn't added yet")
    return _normal_distribution_function_values[result]


_student_distribution_quantiles: dict[int, dict[float, float]] = {
    1: {
        0.750: 1.000
        # ...
    },
    14: {
        0.975: 2.145
    }
    # ...
}


def _get_nearest_key(d: dict, k: float):
    for k_cur in d.keys():
        if abs(k - k_cur) < 1e-5:
            return k_cur
    return None


def student_distribution_coefficient_resolver(n: int, p: float) -> float:
    if n not in _student_distribution_quantiles:
        raise Exception(f"Student coefficients for n={n} haven't added yet")
    ps = _student_distribution_quantiles[n]
    nearest_key = _get_nearest_key(ps, p)
    if nearest_key is None:
        raise Exception(f"Student coefficient for n={n} and p={p} hasn't added yet")
    return ps[nearest_key]


_pearson_distribution_quantiles: dict[int, dict[float, float]] = {
    1: {
        0.005: 0.0000393
        # ...
    },
    14: {
        0.025: 5.63,
        0.975: 26.1
    }
    # ...
}


def pearson_distribution_coefficient_resolver(n: int, p: float) -> float:
    if n not in _pearson_distribution_quantiles:
        raise Exception(f"Pearson coefficients for n={n} haven't added yet")
    ps = _pearson_distribution_quantiles[n]
    nearest_key = _get_nearest_key(ps, p)
    if nearest_key is None:
        raise Exception(f"Pearson coefficient for n={n} and p={p} hasn't added yet")
    return ps[nearest_key]
