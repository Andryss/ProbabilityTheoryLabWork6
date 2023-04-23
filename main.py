import sys

from series_holder import *
from confidence_interval_calculator import *


def print_interval_info(series_info: SeriesInfo, interval_info: ConfidenceIntervalInfo):
    print(f"\n----------RESULT----------")
    print(f"{series_info}:")
    print(f"\nLength: {interval_info.length}")
    print(f"\nSample mean: {interval_info.sample_mean}")
    print(f"Interval: ({interval_info.sample_mean_interval[0]},{interval_info.sample_mean_interval[1]})")
    print(f"\nSample variance: {interval_info.sample_variance}")
    print(f"Interval: ({interval_info.sample_variance_interval[0]},{interval_info.sample_variance_interval[1]})")
    print(f"\nSample deviation: {interval_info.sample_deviation}")


def run_with_series(data: (np.ndarray, float)):
    series_info, upsilon = data
    interval_info = calculate_confident_interval(series_info, upsilon)
    print_interval_info(series_info, interval_info)


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


def run_with_info(data: ((int, float, float), float)):
    series_info, upsilon = data
    fill_empty_info(series_info)
    interval_info = calculate_confident_interval(series_info, upsilon)
    print_interval_info(series_info, interval_info)


def run():
    try:
        run_with_series(get_task1_task7_numbers())
        run_with_info(get_task2_task7_info())
    except Exception as e:
        print(e, file=sys.stderr)


if __name__ == '__main__':
    run()
