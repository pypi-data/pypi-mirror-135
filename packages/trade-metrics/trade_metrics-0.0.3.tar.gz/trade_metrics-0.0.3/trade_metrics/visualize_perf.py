# standard libs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections.abc import Iterable
from sklearn import linear_model
from matplotlib.ticker import FuncFormatter
# own modules
from utils import perf as pm


def compare_performance(
        df1:pd.DataFrame,
        df2:pd.DataFrame,
        start_date:str,
        end_date:str,
        equal_vol:int=1,
        label_df1:str="df1",
        label_df2:str="df2") -> tuple:
    
    """
    Compares performance from a strategy with a benchmark.
    """
    # subset
    df1 = df1[(df1.index > start_date) & (df1.index < end_date)]
    df2 = df2[(df2.index > start_date) & (df2.index < end_date)]
    # make sure the dates allign
    start_date = max(df1.index[0], df2.index[0])
    end_date = min(df1.index[len(df1) - 1], df2.index[len(df2) - 1])
    df1 = df1[(df1.index >= start_date)  & (df1.index <= end_date)]
    df2 = df2[(df2.index >= start_date)  & (df2.index <= end_date)]
    df_ret = df1.copy()
    df_ret[label_df2] = df2
    df_ret.columns = [label_df1, label_df2]
    df_ret.fillna(method="ffill", inplace=True)
    df_ret.fillna(method="bfill", inplace=True)
    # adjust vol
    if equal_vol == 1:
        df_ret[label_df1] = (df_ret[label_df2].std() / df_ret[label_df1].std()) * df_ret[label_df1]
    elif equal_vol == 2:
        df_ret[label_df2] = (df_ret[label_df1].std() / df_ret[label_df2].std()) * df_ret[label_df2]
    elif isinstance(equal_vol, float):
        df_ret[label_df1] = (equal_vol / df_ret[label_df1].std()) * df_ret[label_df1]
        df_ret[label_df2] = (equal_vol / df_ret[label_df2].std()) * df_ret[label_df2]
    # compute performance stats
    perf_strat = df_ret[label_df1].pipe(pm.summary_stats)
    perf_bench = df_ret[label_df2].pipe(pm.summary_stats)
    perf = pd.concat([perf_strat, perf_bench], axis=0)
    perf["corr_pearson"] = df_ret[[label_df1, label_df2]].corr(method="pearson").iloc[0,1]
    perf["corr_spearman"] = df_ret[[label_df1, label_df2]].corr(method="spearman").iloc[0,1]
    perf = perf.T
    perf.columns = [label_df1, label_df2]
    return df_ret, perf


def single_performance_viz(        
        ret_df: pd.DataFrame,
        state: int,float=1,
        vol_adjust: float=0,
        window_rolling: int=126,
        label_df: str="df1",
        color_df: str="#5C588A") -> pd.DataFrame:
    
    """
    """
    # compute cum sum return and drawdown
    df = ret_df.copy()
    df.columns = [label_df]
    if vol_adjust > 0:
        df[label_df] = (vol_adjust / df[label_df].std()) * df[label_df]
    df[f"cumsum_{label_df}"] = (1 + (df[label_df].cumsum()))
    fig, axs = plt.subplots(3, 2, 
                        figsize = (8, 8), 
                        gridspec_kw={
                            'height_ratios':[1.5, 1, 1],
                            'wspace': 0.15}, 
                        sharex=False
                           )
 
    # cum sum return
    axs[0, 0].plot(df.index, df[f"cumsum_{label_df}"], label=f"{label_df} ann. ret. : {df[label_df].mean()*252*100:,.2f}% & vol: {df[label_df].std()*np.sqrt(252)*100:,.2f}%", c=color_df)
    sec_y = axs[0, 0].secondary_yaxis("right")
    sec_y.set_yticks(df[[f"cumsum_{label_df}", f"cumsum_{label_df}"]].round(2).values.tolist()[-1])
    axs[0, 0].set_ylabel("Cum. sum return 1$ investment")
    axs[0, 0].margins(x=0)
    axs[0, 0].yaxis.set_major_formatter(FuncFormatter(lambda x, pos: '%.2f'%x))
    axs[0, 0].legend(ncol=1, loc="best", fontsize=10)
    
    if state == 1 or state == 1.5 or state == 3:
        # drawdown
        df[f"drawdown_{label_df}"] = df[label_df].pipe(pm.drawdown) * 100
        axs[1, 0].plot(df.index, df[f"drawdown_{label_df}"], label=f"{label_df} max. dd: {df[f'drawdown_{label_df}'].max():,.2f}%", c=color_df)
        axs[1, 0].set_ylabel("Drawdown (%)")
        axs[1, 0].yaxis.set_major_formatter(FuncFormatter(lambda x, pos: '%.2f'%x))
        axs[1, 0].margins(x=0)
        axs[1, 0].legend(ncol=2, loc="best", fontsize=10)
    
    if state == 2 or state == 3:
        df[f"rolling_stat_{label_df}"] = df[label_df].rolling(window=window_rolling).apply(pm.sharpe_ratio) * np.sqrt(252)
        if state == 2:
            p = 1
        else:
            p = 2
        # rolling func
        #return df
        axs[p, 0].plot(df.index, df[f"rolling_stat_{label_df}"].replace(np.nan, 0), label=f"{label_df} mean SR: {df[f'rolling_stat_{label_df}'].mean():,.2f}%", c=color_df)
        axs[p, 0].axhline(y=0, color='gray', linestyle='--')
        axs[p, 0].set_ylabel(f"Rolling SR ({window_rolling}D)")
        axs[p, 0].yaxis.set_major_formatter(FuncFormatter(lambda x, pos: '%.2f'%x))
        axs[p, 0].margins(x=0)
        axs[p, 0].legend(ncol=2, loc="best", fontsize=10)
        axs[2, 0].set_xlabel("Date")
        
    if state > 4:
        raise ValueError("Choose valid state (1, 1.5 , 2 or 3")

    return axs

def compare_performance_viz(        
        ret_df1: pd.DataFrame,
        ret_df2: pd.DataFrame,
        start_date: str,
        end_date: str,
        state: int=1,
        vol_adjust: int=1,
        window_rolling: int=126,
        label_df1: str="df1",
        label_df2: str="df2",
        color_df1: str="#5C588A",
        color_df2: str="#f26196",
        style: dict={"Equities": "slategray", "Bonds": "darkcyan", "Credit": "steelblue"}) -> pd.DataFrame:
    
    """
    """
    # get performance data and subset of the strategy
    df, perf = compare_performance(ret_df1, ret_df2, start_date, end_date, vol_adjust, label_df1, label_df2)

    # compute cum sum return and drawdown
    df[f"cumsum_{label_df1}"] = (1 + (df[label_df1].cumsum()))
    df[f"cumsum_{label_df2}"] = (1 + (df[label_df2].cumsum()))


    _, axs = plt.subplots(3, 1, figsize = (8, 10), 
                            gridspec_kw={
                                'height_ratios':[1.5, 1, 1],
                                'wspace': 0.15}, sharex=False);
    
    # cum sum return
    axs[0].plot(df.index, df[f"cumsum_{label_df1}"], label=f"{label_df1} ann. ret. : {df[label_df1].mean()*252*100:,.2f}% & vol: {df[label_df1].std()*np.sqrt(252)*100:,.2f}%", c=color_df1)
    axs[0].plot(df.index, df[f"cumsum_{label_df2}"], label=f"{label_df2} ann. ret. : {df[label_df2].mean()*252*100:,.2f}% & vol: {df[label_df2].std()*np.sqrt(252)*100:,.2f}%", c=color_df2)
    sec_y = axs[0].secondary_yaxis("right")
    sec_y.set_yticks(df[[f"cumsum_{label_df1}", f"cumsum_{label_df2}"]].round(2).values.tolist()[-1])
    axs[0].set_ylabel("Cum. sum return 1$ investment")
    axs[0].margins(x=0)
    axs[0].yaxis.set_major_formatter(FuncFormatter(lambda x, pos: '%.2f'%x))
    axs[0].legend(ncol=1, loc="best", fontsize=10)
    
    if state == 1 or state == 3:
        # drawdown
        df[f"drawdown_{label_df1}"] = df[label_df1].pipe(pm.drawdown) * 100
        df[f"drawdown_{label_df2}"] = df[label_df2].pipe(pm.drawdown) * 100
        axs[1].plot(df.index, df[f"drawdown_{label_df1}"], label=f"{label_df1} max. dd: {df[f'drawdown_{label_df1}'].max():,.2f}%", c=color_df1)
        axs[1].plot(df.index, df[f"drawdown_{label_df2}"], label=f"{label_df2} max. dd: {df[f'drawdown_{label_df2}'].max():,.2f}%", c=color_df2)
        axs[1].set_ylabel("Drawdown (%)")
        axs[1].yaxis.set_major_formatter(FuncFormatter(lambda x, pos: '%.2f'%x))
        axs[1].margins(x=0)
        axs[1].legend(ncol=2, loc="best", fontsize=10)
    
    if state == 1 or state == 2 or state ==3:
        df[f"rolling_stat_{label_df1}"] = df[label_df1].rolling(window=window_rolling).apply(pm.sharpe_ratio) * np.sqrt(252)
        df[f"rolling_stat_{label_df2}"] = df[label_df2].rolling(window=window_rolling).apply(pm.sharpe_ratio) * np.sqrt(252)
        if state == 2:
            p = 1
        else:
            p = 2
        # rolling func
        #return df
        axs[p].plot(df.index, df[f"rolling_stat_{label_df1}"].replace(np.nan, 0), label=f"{label_df1} mean SR: {df[f'rolling_stat_{label_df1}'].mean():,.2f}%", c=color_df1)
        axs[p].plot(df.index, df[f"rolling_stat_{label_df2}"].replace(np.nan, 0), label=f"{label_df2} mean SR: {df[f'rolling_stat_{label_df2}'].mean():,.2f}%", c=color_df2)
        axs[p].axhline(y=0, color='gray', linestyle='--')
        axs[p].set_ylabel(f"Rolling SR ({window_rolling}D)")
        axs[p].yaxis.set_major_formatter(FuncFormatter(lambda x, pos: '%.2f'%x))
        axs[p].margins(x=0)
        axs[p].legend(ncol=1, loc="best", fontsize=10)
        axs[2].set_xlabel("Date")
    
    if state == 2:
        # rolling correlation
        df["rolling_corr"] = df[label_df1].rolling(window_rolling).corr(df[label_df2])
        axs[2].plot(df.index, df["rolling_corr"].replace(np.nan, 0), label=f"Mean corr.: {df['rolling_corr'].mean():,.2f}%", c="black")
        axs[2].axhline(y=0, color='gray', linestyle='--')
        axs[2].set_ylabel(f"Rolling corr. ({window_rolling}D)")
        axs[2].yaxis.set_major_formatter(FuncFormatter(lambda x, pos: '%.2f'%x))
        axs[2].set_xlabel("Date")
        axs[2].margins(x=0)
        axs[2].legend(ncol=1, loc="upper left", fontsize=10)

    
    if state > 4:
        raise ValueError("Choose valid state (1, 1.5 , 2 or 3")

    return axs


