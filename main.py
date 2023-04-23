import sys

from series_holder import *
from confidence_interval_calculator import *


def print_interval_info(interval_info: ConfidenceIntervalInfo):
    print(interval_info.sample_mean)


def run_1():
    series_info = SeriesInfoWithSourceSeries()
    series_info.source_series = get_task1_task7_numbers()
    interval_info = calculate_confident_interval(series_info, 0.95)
    print_interval_info(interval_info)


def run():
    try:
        run_1()
    except Exception as e:
        print(e, file=sys.stderr)


if __name__ == '__main__':
    run()
