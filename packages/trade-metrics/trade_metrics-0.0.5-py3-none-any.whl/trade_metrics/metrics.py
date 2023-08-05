import numpy as np
import pandas as pd
from scipy import stats


def sharpe_ratio(x:pd.DataFrame, freq: float=252.0) -> float:
    """
    Computes Sharpe ratio (SR).
    """
    return (np.mean(x) / np.std(x)) * np.sqrt(freq)

def accuracy(x:pd.Series) -> int:
    """
    Computes the percentage of winning trades.
    """
    return np.mean(x > 0)

def drawdown(x:pd.DataFrame, cumprod:bool=True) -> pd.Series:
    """
    Calculate drawdown.
    """
    if cumprod:
        p = (1 + x).cumprod()
        rm = np.maximum.accumulate(p)
        return 1 - (p / rm)
    else:
        p = 1 + (np.cumsum(x))
        rm = np.maximum.accumulate(p)
        return abs(p - rm)

def max_drawdown(x:pd.DataFrame, cumprod:bool=True) -> float:
    """
    Computes the maximum drawdown.
    """
    return np.max(drawdown(x, cumprod))

def q_mean_drawdown(x:pd.DataFrame, q:float=0.8, cumprod:bool=True) -> pd.Series:
    """
    """
    dd = drawdown(x, cumprod)
    q_dd = np.quantile(dd, q=q)
    return np.mean(dd[dd > q_dd])

def cvar(x:pd.DataFrame, q:float=0.05) -> pd.Series:
    """
    """
    q_var = np.quantile(x, q)
    return np.mean(x[x < q_var])

def max_dd_std_ratio(x:pd.DataFrame, freq: float=252.0) -> float:
    """
    """
    return max_drawdown(x) / (np.std(x) * np.sqrt(freq))

def time_under_water(x:pd.Series) -> pd.Series:
    """
    """
    dd = (drawdown(x) > 0).astype(int)
    return (dd * (dd.groupby((dd != dd.shift(1)).cumsum()).cumcount() + 1))


def summary_stats(x:pd.Series, freq:float=252.0, multiplier:int=100, precision:int=2) -> pd.DataFrame:
    """
    Computes summary stats.
    """
    n = len(x)
    minimum = np.min(x) * multiplier
    maximum = np.max(x) * multiplier
    q_005 = np.quantile(x, 0.05) * multiplier
    q_001 = np.quantile(x, 0.01) * multiplier
    cvar_005 = cvar(x, 0.05) * multiplier
    cvar_001 = cvar(x, 0.01) * multiplier
    median = np.median(x) * multiplier
    mean = np.mean(x) * freq * multiplier
    std = np.std(x) * np.sqrt(freq) *multiplier
    skew = stats.skew(x)
    kurt = stats.kurtosis(x)
    sr = sharpe_ratio(x, freq=freq)
    acc = accuracy(x) * multiplier
    mdd = max_drawdown(x) * multiplier
    calmar_ratio = (mean / multiplier) / mdd
    mdd_std_ratio = max_dd_std_ratio(x, freq=freq)
    q_mean_dd = q_mean_drawdown(x, q=0.8) * multiplier
    max_tuw = time_under_water(x).pipe(max)
    dict_stats =  {
        "count":n, 
        "minimum": minimum, 
        "maximum": maximum, 
        "q_0.05": q_005, 
        "q_0.01": q_001,
        "cvar_0.05": cvar_005,
        "cvar_0.01": cvar_001,
        "median": median,
        "mean": mean, 
        "std": std, 
        "skew": skew,
        "kurtosis": kurt,
        "sharpe_ratio": sr, 
        "accuracy": acc, 
        "maximum_drawdown": mdd,
        "maximum_tuw": max_tuw,
        "calmar_ratio": calmar_ratio,
        "mdd_std_ratio": mdd_std_ratio,
        "mean_drawdown_>_q_0.8": q_mean_dd}

    return pd.DataFrame([dict_stats]).round(precision)


def fix_format(df, index_var=None):
    """
    """
    if index_var is None:
        index_var = df.index.levels[0].name       
    return df.reset_index().set_index(index_var).iloc[:, 1:]