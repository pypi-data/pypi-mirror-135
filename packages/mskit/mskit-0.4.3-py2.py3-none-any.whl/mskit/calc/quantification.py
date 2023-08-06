import typing

import numpy as np
import pandas as pd


def assemble_topn(
        values: typing.Union[list, tuple, np.ndarray, pd.Series],
        topn: typing.Union[int, None, bool] = 3,
        assemble_func: typing.Callable = np.mean,
        nan_value=np.nan,
        thres: typing.Union[int, float, np.ndarray, pd.Series] = 10
):
    """
    topn: int to keep top n items or True for top 3, or others with no action
    """
    values = np.array(values)
    if isinstance(thres, (int, float, np.ndarray, pd.Series)):
        values = values[values > thres]
    elif thres is True:
        values = values[values > 1]

    if len(values) == 0:
        return nan_value
    if isinstance(topn, bool):
        topn = 3 if topn else 0
    if isinstance(topn, int) and topn >= 1:
        values = np.sort(values)[::-1][:topn]
    return assemble_func(values)
