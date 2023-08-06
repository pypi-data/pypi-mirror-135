import wcorr
import pandas as pd


def profit_func(
    data,
    pred="pred",
    long_profit="long_profit_fwd1",
    short_profit="short_profit_fwd1",
    weight="w",
    cost=0.0,
    **kwargs,
):
    long_profit = (
        (data[pred] > 0).astype(int) * (data[long_profit] - cost) * data[weight]
    )
    short_profit = (
        (data[pred] < 0).astype(int) * (data[short_profit] - cost) * data[weight]
    )
    return sum(long_profit + short_profit) / sum(data[weight])


def ic_func(data, pred="pred", label="label", weight="w", **kwargs):
    return wcorr.wspearman(data[pred], data[label], data[weight])


def get_n_largest_cond(
    data,
    amount_th=1e5,
    n=25,
    amount="Amount",
    dcol="Date",
    rank="pred_abs",
    rank_th=0,
    **kwargs,
):
    amount_cond = (data[amount] > amount_th) & (data[rank] > rank_th)
    return (
        data[amount_cond].groupby(dcol)[rank].nlargest(n).droplevel(2).index.swaplevel()
    )


def gen_daily_frame(data, func, dcol="Date", pred="pred", amount="Amount", **kwargs):
    data["pred_abs"] = data[pred].abs()
    data["w"] = data["pred_abs"] * data["Amount"]
    n_largest_cond = get_n_largest_cond(data, dcol=dcol, amount=amount, **kwargs)
    return data.loc[n_largest_cond].groupby(dcol).apply(lambda x: func(x, **kwargs))


def gen_daily_profit_df(data, idx_name="", **kwargs):
    frame = gen_daily_frame(data, func=profit_func, **kwargs)
    df = pd.DataFrame(frame, columns=["profit"])
    if idx_name:
        df["Set"] = idx_name
        df = df.reset_index().set_index(["Set", "Date"])
    return df


def gen_daily_ic_df(data, idx_name="", n=650, **kwargs):
    frame = gen_daily_frame(data, func=ic_func, n=n, **kwargs)
    df = pd.DataFrame(frame, columns=["ic"])
    if idx_name:
        df["Set"] = idx_name
        df = df.reset_index().set_index(["Set", "Date"])
    return df


def concat_dfs(datas, col="profit", rolling_period=21, **kwargs):
    daily_profit = pd.DataFrame(pd.concat(datas), columns=[col])
    daily_profit[f"rolling_{col}"] = daily_profit.rolling(rolling_period)[col].mean()
    return daily_profit
