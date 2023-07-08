# %%
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axes import Axes


def plot(region, ax: Axes):
    data = json.load(Path(Rf"../../logs/rank/bikini_{region}.json").open())
    df_data = dict()
    for record in data:
        df_record = dict()
        for target in range(1, 18):
            for typ in [1, 2]:
                targets = record["data"][f"bikini_vote_type{typ}_total"]
                cnt = int(targets[f"target_{target}"])
                df_record[(target, typ)] = cnt
        df_data[datetime.fromtimestamp(record["time"])] = df_record

    # %%
    df = pd.DataFrame.from_dict(df_data, orient="index")
    # %%
    gun_style = {
        "M1903": ("#8c564b", "-"),
        "WA2000": ("#d62728", "-"),
        "FN49": ("#ff7f0e", "--"),
        "NTW20": ("#e377c2", "-"),
        "G41": ("#d62728", "--"),
        "G36": ("#ff7f0e", "-"),
        "FNFAL": ("#8c564b", "--"),
        "95type": ("#7f7f7f", "-"),
        "FN57": ("#7f7f7f", "--"),
        "G28": ("#2ca02c", "-"),
        "AA12": ("#17becf", "-"),
        "CBJMS": ("#17becf", "--"),
        "UKM2000": ("#e377c2", "--"),
        "4type": ("#9467bd", "-"),
        "DP12": ("#1f77b4", "-"),
        "KAC": ("#9467bd", "--"),
        "PPD40": ("#bcbd22", "-"),
    }
    guns = list(gun_style.keys())
    df_total = pd.concat(
        [pd.Series(df[(i, 1)] + df[i, 2], name=guns[i - 1]) for i in range(1, 18)],
        axis=1,
    )
    df_total.sort_index(
        axis=1, key=lambda x: df_total.iloc[-1][x], ascending=False, inplace=True
    )
    # %%
    ax.set_title(f"{region} server", fontsize=40)
    ax.ticklabel_format(style="plain", axis="y")
    ax.grid()
    ax.xaxis.set_tick_params(labelbottom=True)
    for i in df_total:
        ax.plot(df_total[i], label=i, linestyle=gun_style[i][1], color=gun_style[i][0])
    ax.legend()


# %%
fig, axes = plt.subplots(3, 1, figsize=(16, 27), sharex=True)
for region, ax in zip(["cn", "tw", "kr"], axes):
    plot(region, ax)
    plt.savefig("bikini.png")
