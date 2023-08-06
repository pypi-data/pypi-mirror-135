import re
import typing

import numpy as np
import pandas as pd
import dask.dataframe as dd

from mskit import rapid_kit as rk
from ._maxquant import maxquant_constants

"""
检索结果的导入
    1. 每种文件单独
    2. 所有文件在一个文件夹中，读入指定文件关联 id

"""


def select_prec_from_multi_match(
        df: pd.DataFrame,
        max_match: int = 1,
        rt_window: int = 6,
        rt_group_col: typing.Union[tuple, list, str] = ('Experiment', 'Modified sequence'),
        rt_baseline_func: typing.Callable = np.median,
        rt_col: str = 'Retention time',
        restrict_group_col: typing.Union[tuple, list, str] = ('Experiment', 'Replicates', 'Prec'),
        extra_selection_col: str = 'Score',
        keep_explicit_intermediate_cols: bool = False,
        dask_npart: int = None,
        report: bool = False,
):
    """
    rt_window: int or None, full window in minute
    rt_main_group_col: str or None
    """
    if keep_explicit_intermediate_cols:
        rt_diff_col = 'RT-Diff'
    else:
        rt_diff_col = rk.get_random_string(exclude=df.columns.tolist())
    raw_idx_col = rk.get_random_string(exclude=[*df.columns.tolist(), rt_diff_col])
    df[raw_idx_col] = df.index.values.copy()
    raw_idx_name = df.index.name
    df = df.reset_index(drop=True)
    df[rt_diff_col] = df[rt_col].values - df.groupby(list(rt_group_col))[rt_col].transform(rt_baseline_func).values
    if dask_npart is not None:
        _df = dd.from_pandas(df, npartitions=dask_npart)
        idx = _df.groupby(list(restrict_group_col))[rt_diff_col].apply(lambda x: x.abs().idxmin(), meta=('idx', 'int')).values.compute()
    else:
        idx = df.groupby(list(restrict_group_col))[rt_diff_col].apply(lambda x: x.abs().idxmin()).values
    df = df.loc[idx]
    df.index = df[raw_idx_col]
    df.index = df.index.rename(raw_idx_name)
    df = df.drop(columns=raw_idx_col)
    if not keep_explicit_intermediate_cols:
        df = df.drop(columns=rt_diff_col)
    return df


def ion_info_from_mq(need_ion_type=('b', 'y'), verify_mass=True, verify_tolerance=20):
    pass


def inten_from_mq(x):
    ions = x['Matches']
    intens = x['Intensities']

    ion_intens_list = list(zip(ions.split(';'), intens.split(';')))

    inten_dict = dict()

    for ion_type in ['b', 'y']:
        ion_info = [_ for _ in ion_intens_list if _[0].startswith(ion_type)]

        current_num = 0
        ex_mod = 0
        for ion, inten in ion_info:

            ion_num = re.findall(f'{ion_type}(\d+)', ion)[0]
            ion_num = int(ion_num)

            re_charge = re.findall('\((\d)\+\)', ion)
            if re_charge:
                ion_charge = re_charge[0]
            else:
                ion_charge = '1'

            frag = f'{ion_type}{ion_num}+{ion_charge}'

            if '-' in ion:
                loss_type = re.findall('-(.+)$', ion)[0]
                frag += f'-1,{loss_type}'
                if ex_mod:
                    frag += f';{ex_mod},H3PO4'

            elif '*' in ion:
                if ex_mod == 0:
                    current_num = 0
                    ex_mod = 1
                else:
                    if ion_num <= current_num:
                        ex_mod += 1
                frag += f'-{ex_mod},H3PO4'

            else:
                frag += f'-Noloss'

            current_num = ion_num

            inten_dict[frag] = float(inten)

    return inten_dict


def show_ion_pair(result_df, iloc, return_df=True):
    ion_pairs = list(zip(result_df.iloc[iloc]['Masses'].split(';'),
                         result_df.iloc[iloc]['Matches'].split(';'),
                         result_df.iloc[iloc]['Intensities'].split(';')))
    if return_df:
        return pd.DataFrame(ion_pairs, columns=['FragMz', 'Frag', 'Inten'])
    else:
        for _ in ion_pairs:
            print(_)


def remove_reverse_hits(evi_msms: pd.DataFrame):
    return evi_msms.loc[evi_msms['Reverse'] != '+']


def remove_zero_inten_hits(evi_msms: pd.DataFrame):
    return evi_msms.loc[evi_msms['Intensity'] > 0]
