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


def run_with_series():
    series_info = SeriesInfoWithSourceSeries()
    series_info.source_series, upsilon = get_test_task_numbers()
    interval_info = calculate_confident_interval(series_info, upsilon)
    print_interval_info(series_info, interval_info)


def run_with_info():
    series_info = SeriesInfoWithCharacteristics()
    (series_info.length, series_info.series_sum, series_info.series_squares_sum), upsilon = get_test_task_info()
    interval_info = calculate_confident_interval(series_info, upsilon)
    print_interval_info(series_info, interval_info)


def run():
    try:
        run_with_series()
        run_with_info()
    except Exception as e:
        print(e, file=sys.stderr)


if __name__ == '__main__':
    run()
