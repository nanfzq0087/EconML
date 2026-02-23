# -*- coding: utf-8 -*-
"""
Download SPX (S&P 500 index) data via yfinance, save locally, and plot each variable.

Outputs:
- raw_data/^GSPC_<start>_<end>_1d.csv
- figures/<column>.png (one plot per variable)

Usage:
    python3 download_data.py --ticker ^GSPC --period max --interval 1d
"""

import os
import argparse
from datetime import datetime

import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt


def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def safe_filename(s):
    if isinstance(s, tuple):
        s = "_".join([str(x) for x in s])
    return str(s).replace("^", "").replace("/", "_").replace(" ", "_")


def fetch_spx(
    ticker: str,
    interval: str,
    start: str | None,
    end: str | None,
    period: str | None,
) -> pd.DataFrame:
    # yfinance allows either (start, end) or period
    df = yf.download(
        tickers=ticker,
        start=start,
        end=end,
        period=period,
        interval=interval,
        auto_adjust=False,
        progress=False,
        threads=True,
    )

    if df is None or df.empty:
        raise RuntimeError("No data returned. Check ticker / network / date range.")

    # Ensure clean index/columns
    df = df.copy()
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    # Keep only numeric columns (multivariate)
    df = df.select_dtypes(include="number")
    return df


def plot_each_column(df, out_dir, title_prefix=""):
    import math
    import matplotlib.pyplot as plt
    import os

    os.makedirs(out_dir, exist_ok=True)

    cols = df.columns
    n = len(cols)

    if n == 0:
        print("No columns to plot.")
        return

    # 自动布局：最多3列
    ncols = 3
    nrows = math.ceil(n / ncols)

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(5 * ncols, 3 * nrows))

    # 如果只有一行或一列，需要处理axes形状
    if nrows == 1 and ncols == 1:
        axes = [[axes]]
    elif nrows == 1:
        axes = [axes]
    elif ncols == 1:
        axes = [[ax] for ax in axes]

    axes = [ax for row in axes for ax in row]  # flatten

    for i, col in enumerate(cols):
        series = df[col].dropna()
        axes[i].plot(series.index, series.values)
        axes[i].set_title(f"{title_prefix}{col}")
        axes[i].tick_params(axis='x', rotation=30)

    # 多余子图隐藏
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)

    plt.tight_layout()
    out_path = os.path.join(out_dir, "all_variables.png")
    plt.savefig(out_path, dpi=200)
    plt.close()

    print(f"[OK] Saved combined plot: {out_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker", type=str, default="^GSPC", help="SPX ticker on Yahoo Finance")
    parser.add_argument("--interval", type=str, default="1d", help="e.g., 1d, 1h, 5m")
    parser.add_argument("--start", type=str, default=None, help="YYYY-MM-DD (optional if --period is used)")
    parser.add_argument("--end", type=str, default=None, help="YYYY-MM-DD (optional if --period is used)")
    parser.add_argument("--period", type=str, default=None, help="e.g., 1y, 5y, 10y, max (optional)")
    parser.add_argument("--out_data_dir", type=str, default="raw_data")
    parser.add_argument("--out_fig_dir", type=str, default="raw_data//raw_figures")
    args = parser.parse_args()

    ensure_dir(args.out_data_dir)
    ensure_dir(args.out_fig_dir)

    df = fetch_spx(
        ticker=args.ticker,
        interval=args.interval,
        start=args.start,
        end=args.end,
        period=args.period,
    )

    # Save CSV
    # Decide label for filename
    if args.period:
        tag = args.period
    else:
        start_tag = args.start or df.index.min().strftime("%Y-%m-%d")
        end_tag = args.end or df.index.max().strftime("%Y-%m-%d")
        tag = f"{start_tag}_{end_tag}"

    fname = f"{safe_filename(args.ticker)}_{tag}_{args.interval}.csv"
    csv_path = os.path.join(args.out_data_dir, fname)
    df.to_csv(csv_path, index=True)

    # Plot each variable
    title_prefix = f"{args.ticker} ({args.interval}) - "
    fig_subdir = os.path.join(args.out_fig_dir, f"{safe_filename(args.ticker)}_{tag}_{args.interval}")
    plot_each_column(df, fig_subdir, title_prefix=title_prefix)

    print(f"[OK] Saved data: {csv_path}")
    print(f"[OK] Saved plots to folder: {fig_subdir}")
    print(f"Columns: {list(df.columns)}")
    print(f"Rows: {len(df)} | Range: {df.index.min().date()} -> {df.index.max().date()}")


if __name__ == "__main__":
    main()