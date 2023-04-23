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
    pass


class SeriesInfoWithSourceSeries(SeriesInfo):
    source_series: np.ndarray


class SeriesInfoWithCharacteristics(SeriesInfo):
    length: int
    series_sum: float
    series_squares_sum: float


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

    confidence_interval_info.sample_mean = series_info.series_sum / series_info.length

    confidence_interval_info.sample_variance = \
        series_info.series_squares_sum / series_info.length - confidence_interval_info.sample_mean ** 2

    confidence_interval_info.sample_deviation = math.sqrt(confidence_interval_info.sample_variance)

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
    corrected_sample_variance = interval_info.length / (interval_info.length - 1) * interval_info.sample_variance
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
        interval_info.length * corrected_sample_variance ** 2 / xi_left,
        interval_info.length * corrected_sample_variance ** 2 / xi_right
    )
