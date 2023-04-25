import sys

from series_holder import *
from confidence_interval_calculator import *
from distribution_holder import *
from distribution_checker import *


def print_interval_info(series_info: SeriesInfo, upsilon: float, interval_info: ConfidenceIntervalInfo):
    print(f"\n----------RESULT----------")
    print(f"{series_info}:")
    print(f"upsilon: {upsilon}")
    print(f"\nLength: {interval_info.length}")
    print(f"\nSample mean: {interval_info.sample_mean}")
    print(f"Interval: ({interval_info.sample_mean_interval[0]},{interval_info.sample_mean_interval[1]})")
    print(f"\nSample variance: {interval_info.sample_variance}")
    print(f"Interval: ({interval_info.sample_variance_interval[0]},{interval_info.sample_variance_interval[1]})")
    print(f"\nSample deviation: {interval_info.sample_deviation}")


def run_with_series(data: (SeriesInfoWithSourceSeries, float)):
    series_info, upsilon = data
    interval_info = calculate_confident_interval(series_info, upsilon)
    print_interval_info(series_info, upsilon, interval_info)


def fill_empty_info(series_info: SeriesInfoWithCharacteristics):
    if series_info.length is None:
        raise Exception("Length is None")
    if series_info.series_sum is None and \
            series_info.sample_mean is None:
        raise Exception("Series sum and sample mean can't both be None")
    if series_info.series_squares_sum is None and \
            series_info.series_centered_squares_sum is None and \
            series_info.sample_derivative is None:
        raise Exception("Squares sum and centered squares sum and sample derivative can't together be None")

    if series_info.series_sum is None:
        series_info.series_sum = series_info.sample_mean * series_info.length
    if series_info.sample_mean is None:
        series_info.sample_mean = series_info.series_sum / series_info.length

    if series_info.sample_derivative is None:
        if series_info.series_squares_sum is not None:
            series_info.sample_derivative = \
                math.sqrt(series_info.series_squares_sum / series_info.length - series_info.sample_mean ** 2)
        else:
            series_info.sample_derivative = series_info.series_centered_squares_sum / series_info.length
    if series_info.series_centered_squares_sum is None:
        series_info.series_centered_squares_sum = series_info.sample_derivative * series_info.length
    if series_info.series_squares_sum is None:
        series_info.series_squares_sum = \
            (series_info.sample_derivative ** 2 + series_info.sample_mean ** 2) * series_info.length


def run_with_info(data: (SeriesInfoWithCharacteristics, float)):
    series_info, upsilon = data
    fill_empty_info(series_info)
    interval_info = calculate_confident_interval(series_info, upsilon)
    print_interval_info(series_info, upsilon, interval_info)


def print_poisson_distribution_result(distribution_check_result: PoissonDistributionCheckResult):
    if distribution_check_result.source_distribution.shape[0] < 30:
        pd.set_option('display.expand_frame_repr', False)

    print(f"\n----------RESULT----------")
    print(f"\nSource distribution:")
    print(f"{distribution_check_result.source_distribution.set_index('i').T}")
    print(f"Upsilon: {distribution_check_result.upsilon}")
    print(f"\nLambda parameter: {distribution_check_result.sample_lambda}")
    print(f"\nTheoretical poisson distribution:\n{distribution_check_result.theoretical_distribution.set_index('i').T}")
    print(f"\nChi2 observable: {distribution_check_result.chi2_observable}")
    print(f"Chi2 critical: {distribution_check_result.chi2_critical}")
    print(f"\nVerdict (is poisson distribution?): {distribution_check_result.is_poisson_distribution}")


def print_distribution_result(distribution_check_result: DistributionCheckResult):
    if isinstance(distribution_check_result, PoissonDistributionCheckResult):
        print_poisson_distribution_result(distribution_check_result)
    else:
        raise Exception(f"No printer for distribution result class {distribution_check_result.__class__}")


def run_with_distribution(data: (DistributionInfo, float)):
    distribution_info, upsilon = data
    distribution_check_result = distribution_check(distribution_info, upsilon)
    print_distribution_result(distribution_check_result)


def run():
    try:
        run_with_series(get_task1_task7_numbers())
        run_with_info(get_task2_task7_info())
        run_with_distribution(get_task3_task17_distribution())
    except Exception as e:
        print(e, file=sys.stderr)


if __name__ == '__main__':
    run()
