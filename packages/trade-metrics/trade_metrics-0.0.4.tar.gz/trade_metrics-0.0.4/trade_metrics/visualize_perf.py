# standard libs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import metrics


def single_performance_viz(        
        ret_df: pd.DataFrame,
        vol_adjust: float=0,
        window_rolling: int=126,
        freq: float=252,
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
    _, axs = plt.subplots(3, 1, 
                        figsize = (8, 8), 
                        gridspec_kw={
                            'height_ratios':[1.5, 1, 1],
                            'wspace': 0.15}, 
                        sharex=False
                           )
 
    # cum sum return
    axs[0].plot(df.index, df[f"cumsum_{label_df}"], label=f"{label_df} ann. ret. : {df[label_df].mean()*freq*100:,.2f}% & vol: {df[label_df].std()*np.sqrt(freq)*100:,.2f}%", c=color_df)
    sec_y = axs[0].secondary_yaxis("right")
    sec_y.set_yticks(df[[f"cumsum_{label_df}", f"cumsum_{label_df}"]].round(2).values.tolist()[-1])
    axs[0].set_ylabel("Cum. sum return 1$ investment")
    axs[0].margins(x=0)
    axs[0].yaxis.set_major_formatter(FuncFormatter(lambda x, pos: '%.2f'%x))
    axs[0].legend(ncol=1, loc="best", fontsize=10)
    
    # drawdown
    df[f"drawdown_{label_df}"] = df[label_df].pipe(metrics.drawdown) * 100
    axs[1].plot(df.index, df[f"drawdown_{label_df}"], label=f"{label_df} max. dd: {df[f'drawdown_{label_df}'].max():,.2f}%", c=color_df)
    axs[1].set_ylabel("Drawdown (%)")
    axs[1].yaxis.set_major_formatter(FuncFormatter(lambda x, pos: '%.2f'%x))
    axs[1].margins(x=0)
    axs[1].legend(ncol=2, loc="best", fontsize=10)

    # rolling sharpe
    df[f"rolling_stat_{label_df}"] = df[label_df].rolling(window=window_rolling).apply(metrics.sharpe_ratio, args=(freq,))
    axs[2].plot(df.index, df[f"rolling_stat_{label_df}"].replace(np.nan, 0), label=f"{label_df} mean SR: {df[f'rolling_stat_{label_df}'].mean():,.2f}%", c=color_df)
    axs[2].axhline(y=0, color='gray', linestyle='--')
    axs[2].set_ylabel(f"Rolling SR ({window_rolling}P)")
    axs[2].yaxis.set_major_formatter(FuncFormatter(lambda x, pos: '%.2f'%x))
    axs[2].margins(x=0)
    axs[2].legend(ncol=2, loc="best", fontsize=10)
    axs[2].set_xlabel("Date")

    return axs

