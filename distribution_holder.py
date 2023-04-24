from distribution_checker import *


def get_task_test_distribution() -> (DistributionInfo, float):
    return (
        DistributionInfo(
            pd.DataFrame(data={
                'i': [0, 1, 2, 3, 4, 5],
                'n_i': [427, 235, 72, 21, 1, 1]
            })
        ),
        0.01
    )
