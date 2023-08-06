import seaborn as sns


def plot_daily_frame(data, col="", year_n=250):
    sns.set(rc={"figure.figsize": (12, 8)})
    # sns.set_style("white")
    if not col:
        col = data.columns[0]
    sets = data.index.get_level_values(0).unique()
    profit_mean = data[col].mean()
    profit_std = data[col].std()
    year_rolling = data.rolling(year_n)[col].mean()
    for i, s in enumerate(sets):
        df_set = data.loc[s]
        p = sns.lineplot(data=df_set, style="white")
        p.plot(year_rolling.loc[s], color="black")
        p.axvline(df_set.index.max(), color="g")
        p.axhline(0, color="r")
        p.axhline(profit_mean, color="w")
        if i == 0:
            p.set_title(f"mean: {profit_mean: 0.4f} std: {profit_std: 0.4f}")
            p.text(
                df_set.index[0],
                profit_mean,
                f"{profit_mean: .04f}",
                ha="right",
                va="center",
                color="b",
            )
