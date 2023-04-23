from confidence_interval_calculator import *


def get_test_task_numbers() -> (SeriesInfoWithSourceSeries, float):
    return (
        SeriesInfoWithSourceSeries(
            np.array([162, 151, 161, 170, 167, 164, 166, 164, 173, 172])
        ),
        0.95
    )


def get_task1_task7_numbers() -> (SeriesInfoWithSourceSeries, float):
    return (
        SeriesInfoWithSourceSeries(
            np.array([79, 86, 87, 90, 82, 88, 73, 91, 94, 92, 100, 83, 96, 89, 78])
        ),
        0.95
    )


def get_test_task_info() -> (SeriesInfoWithCharacteristics, float):
    return (
        SeriesInfoWithCharacteristics(
            72, 1267.2, None, 22536, None, None
        ),
        0.99
    )


def get_task2_task7_info() -> (SeriesInfoWithCharacteristics, float):
    return (
        SeriesInfoWithCharacteristics(
            80, None, 69, None, None, 4
        ),
        0.99
    )
