import numpy as np


def get_test_task_numbers() -> (np.ndarray, float):
    return (
        np.array([162, 151, 161, 170, 167, 164, 166, 164, 173, 172]),
        0.95
    )


def get_task1_task7_numbers() -> (np.ndarray, float):
    return (
        np.array([79, 86, 87, 90, 82, 88, 73, 91, 94, 92, 100, 83, 96, 89, 78]),
        0.95
    )


def get_test_task_info() -> ((int, float, float), float):
    return (
        (72, 1267.2, 22536),
        0.99
    )


def get_task2_task7_info() -> ((int, float, float), float):
    return (
        (80, 69, 4),
        0.99
    )
