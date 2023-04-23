import math

import numpy as np

from coefficient_resolvers import *


class ConfidenceIntervalInfo:
    length: int
    sample_mean: float
    sample_mean_interval: (float, float)
    sample_variance: float
    sample_variance_interval: (float, float)
    sample_deviation: float


class SeriesInfo:

    def __str__(self) -> str:
        return "<empty series>"


class SeriesInfoWithSourceSeries(SeriesInfo):
    source_series: np.ndarray

    def __init__(self, ss) -> None:
        self.source_series = ss

    def __str__(self) -> str:
        return f"series {self.source_series}"


class SeriesInfoWithCharacteristics(SeriesInfo):
    length: int

    series_sum: float
    sample_mean: float

    series_squares_sum: float
    series_centered_squares_sum: float
    sample_derivative: float

    _source_string: str

    def __init__(self, ln, ss, sm, sss, scss, sd) -> None:
        self.length = ln
        self.series_sum, self.sample_mean = ss, sm
        self.series_squares_sum, self.series_centered_squares_sum, self.sample_derivative = sss, scss, sd
        self._source_string = f"series with" \
               f"{f' length {self.length}' if self.length is not None else ''}" \
               f"{f' sum {self.series_sum}' if self.series_sum is not None else ''}" \
               f"{f' mean {self.sample_mean}' if self.sample_mean is not None else ''}" \
               f"{f' squares sum {self.series_squares_sum}' if self.series_squares_sum is not None else ''}" \
               f"{f' centered squares sum {self.series_centered_squares_sum}' if self.series_centered_squares_sum is not None else ''}" \
               f"{f' derivative {self.sample_derivative}' if self.sample_derivative is not None else ''}"

    def __str__(self) -> str:
        return self._source_string


def calculate_confident_interval(series_info: SeriesInfo, upsilon: float) -> ConfidenceIntervalInfo:
    assert 0.0 <= upsilon < 1, "Upsilon must be in range [0;1)"
    if isinstance(series_info, SeriesInfoWithSourceSeries):
        return calculate_confident_interval_from_source_series(series_info, upsilon)
    elif isinstance(series_info, SeriesInfoWithCharacteristics):
        return calculate_confident_interval_from_characteristics(series_info, upsilon)
    else:
        raise Exception("Unsupported type of SeriesInfo")


def calculate_confident_interval_from_source_series(series_info: SeriesInfoWithSourceSeries,
                                                    upsilon: float) -> ConfidenceIntervalInfo:
    confidence_interval_info = ConfidenceIntervalInfo()
    series = series_info.source_series.reshape(-1)

    confidence_interval_info.length = len(series)

    confidence_interval_info.sample_mean = series.sum() / confidence_interval_info.length

    series_squared = series * series
    confidence_interval_info.sample_variance = \
        series_squared.sum() / confidence_interval_info.length - confidence_interval_info.sample_mean ** 2

    confidence_interval_info.sample_deviation = math.sqrt(confidence_interval_info.sample_variance)

    calculate_confident_intervals(confidence_interval_info, upsilon)

    return confidence_interval_info


def calculate_confident_interval_from_characteristics(series_info: SeriesInfoWithCharacteristics,
                                                      upsilon: float) -> ConfidenceIntervalInfo:
    confidence_interval_info = ConfidenceIntervalInfo()

    confidence_interval_info.length = series_info.length

    confidence_interval_info.sample_mean = series_info.sample_mean

    confidence_interval_info.sample_variance = series_info.sample_derivative ** 2

    confidence_interval_info.sample_deviation = series_info.sample_derivative

    calculate_confident_intervals(confidence_interval_info, upsilon)

    return confidence_interval_info


_sample_border = 30


def calculate_confident_intervals(interval_info: ConfidenceIntervalInfo, upsilon: float):
    if interval_info.length <= _sample_border:
        calculate_mean_interval_tiny_sample(interval_info, upsilon)
    else:
        calculate_mean_interval_giant_sample(interval_info, upsilon)
    calculate_variance_interval(interval_info, upsilon)


def calculate_mean_interval_tiny_sample(interval_info: ConfidenceIntervalInfo, upsilon: float):
    corrected_sample_variance = \
        math.sqrt(interval_info.length / (interval_info.length - 1) * interval_info.sample_variance)
    t_student = student_distribution_coefficient_resolver(interval_info.length - 1, (1 + upsilon) / 2)
    mean_range = t_student * corrected_sample_variance / math.sqrt(interval_info.length)
    interval_info.sample_mean_interval = (
        interval_info.sample_mean - mean_range,
        interval_info.sample_mean + mean_range
    )


def calculate_mean_interval_giant_sample(interval_info: ConfidenceIntervalInfo, upsilon: float):
    t_upsilon = normal_distribution_function_coefficient_resolver((1 + upsilon) / 2)
    mean_range = t_upsilon * interval_info.sample_deviation / math.sqrt(interval_info.length)
    interval_info.sample_mean_interval = (
        interval_info.sample_mean - mean_range,
        interval_info.sample_mean + mean_range
    )


def calculate_variance_interval(interval_info: ConfidenceIntervalInfo, upsilon: float):
    corrected_sample_variance = interval_info.length / (interval_info.length - 1) * interval_info.sample_variance
    xi_left = pearson_distribution_coefficient_resolver(interval_info.length - 1, (1 + upsilon) / 2)
    xi_right = pearson_distribution_coefficient_resolver(interval_info.length - 1, (1 - upsilon) / 2)
    interval_info.sample_variance_interval = (
        interval_info.length * corrected_sample_variance / xi_left,
        interval_info.length * corrected_sample_variance / xi_right
    )
