import math

import pandas as pd
from pandas.api import types

from coefficient_resolvers import pearson_distribution_coefficient_resolver


class DistributionInfo:
    data: pd.DataFrame

    def __init__(self, d) -> None:
        self.data = d


class DistributionCheckResult:
    source_distribution: pd.DataFrame


class PoissonDistributionCheckResult(DistributionCheckResult):
    sample_lambda: float
    number_of_groups_after_merge: int
    chi2_observable: float
    chi2_critical: float
    is_poisson_distribution: bool


def poisson_distribution_check(distribution_info: DistributionInfo, upsilon: float) -> PoissonDistributionCheckResult:
    data = distribution_info.data
    distribution_result = PoissonDistributionCheckResult()
    distribution_result.source_distribution = data.copy()

    number_of_samples = data['n_i'].sum()
    lmbd = (data['i'] * data['n_i']).sum() / number_of_samples

    distribution_result.sample_lambda = lmbd
    theoretical_data = data.assign(p_i=lambda col: col['i'].map(lambda val: lmbd ** val) / col['i'].map(lambda val: math.factorial(val)) * math.exp(-lmbd))
    theoretical_data = theoretical_data.assign(n_i_thr=lambda col: round(col['p_i'] * number_of_samples))

    merge_row = theoretical_data.shape[0] - 1
    new_n_i, new_p_i, new_n_i_thr = theoretical_data.at[merge_row, 'n_i'], theoretical_data.at[merge_row, 'p_i'], theoretical_data.at[merge_row, 'n_i_thr']
    while number_of_samples * new_p_i < 5:
        merge_row -= 1
        new_n_i += theoretical_data.at[merge_row, 'n_i']
        new_p_i += theoretical_data.at[merge_row, 'p_i']
        new_n_i_thr += theoretical_data.at[merge_row, 'n_i_thr']

    merged_data = theoretical_data.drop(index=range(merge_row, theoretical_data.shape[0]))
    merged_data.loc[merge_row] = [-1, new_n_i, new_p_i, new_n_i_thr]

    merged_data = merged_data.drop(['p_i'], axis=1).assign(chi2_i=lambda col: (col['n_i'] - col['n_i_thr']) ** 2 / col['n_i_thr'])
    distribution_result.number_of_groups_after_merge = len(merged_data)

    chi2_observable = merged_data['chi2_i'].sum()
    distribution_result.chi2_observable = chi2_observable

    chi2_critical = pearson_distribution_coefficient_resolver(distribution_result.number_of_groups_after_merge - 1 - 1, 1 - upsilon)
    distribution_result.chi2_critical = chi2_critical

    distribution_result.is_poisson_distribution = chi2_observable < chi2_critical

    return distribution_result


def distribution_check(distribution_info: DistributionInfo, upsilon: float) -> DistributionCheckResult:
    data = distribution_info.data
    cols = data.columns
    assert cols.size == 2 and cols[0] == 'i' and cols[1] == 'n_i', "Columns must be (i, n_i)"
    assert all(data.notnull()), "Must contains only non null values"
    assert types.is_numeric_dtype(data['i']) and types.is_numeric_dtype(data['n_i']), "Must have numeric values"
    return poisson_distribution_check(distribution_info, upsilon)
