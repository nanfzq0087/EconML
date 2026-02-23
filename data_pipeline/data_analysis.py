# -*- coding: utf-8 -*-
"""
data_analysis.py (Basic v1)
Only includes:
- Layer 1: Structural inspection (range, shape, freq guess, missingness)
- Layer 2: Descriptive statistics (describe + skew + kurtosis)

Outputs:
- <out_dir>/report.json
- <out_dir>/missingness.csv
- <out_dir>/stats.csv

Usage:
  python3 data_analysis.py --input raw_data/GSPC_max_1d.csv --out_dir analysis/GSPC_1d
"""

import os
import re
import json
import argparse
from typing import Dict

import pandas as pd


# -------------------------
# Utils
# -------------------------
def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def flatten_colname(col) -> str:
    """Make column names safe and consistent."""
    if isinstance(col, tuple):
        col = "_".join(str(x) for x in col)
    col = str(col).strip()
    col = col.replace(" ", "_").replace("/", "_")
    col = re.sub(r"_+", "_", col).strip("_")
    return col


def guess_time_freq(dt_index: pd.DatetimeIndex) -> str:
    """Best-effort frequency guess (not guaranteed)."""
    if len(dt_index) < 3:
        return "unknown"
    diffs = pd.Series(dt_index[1:] - dt_index[:-1]).dropna()
    if diffs.empty:
        return "unknown"
    mode = diffs.mode()
    if mode.empty:
        return "unknown"
    delta = mode.iloc[0]

    if delta <= pd.Timedelta(minutes=1):
        return "1min"
    if delta <= pd.Timedelta(minutes=5):
        return "5min_or_less"
    if delta <= pd.Timedelta(hours=1):
        return "hourly_or_less"
    if delta <= pd.Timedelta(days=1):
        return "daily_or_less"
    if delta <= pd.Timedelta(days=7):
        return "weekly_or_less"
    return "low_freq"


def safe_to_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """Coerce all columns to numeric where possible."""
    out = df.copy()
    for c in out.columns:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    return out


# -------------------------
# Core
# -------------------------
def load_timeseries_csv(path: str) -> pd.DataFrame:
    """
    Load CSV and return a DataFrame indexed by datetime.
    Accepts either:
    - explicit "Date" / "Datetime" column
    - first column looks like datetime (e.g., index saved to CSV)
    """
    df = pd.read_csv(path)

    # Try common datetime column names first
    dt_col = None
    for cand in ["Datetime", "datetime", "Date", "date", "timestamp", "Timestamp"]:
        if cand in df.columns:
            dt_col = cand
            break

    if dt_col is not None:
        df[dt_col] = pd.to_datetime(df[dt_col], errors="coerce")
        df = df.dropna(subset=[dt_col]).set_index(dt_col)
    else:
        # Assume first column is index-like datetime
        first = df.columns[0]
        dt = pd.to_datetime(df[first], errors="coerce")  # may warn; OK
        if dt.notna().mean() > 0.9:
            df[first] = dt
            df = df.dropna(subset=[first]).set_index(first)
        else:
            raise ValueError(
                "Could not infer a DatetimeIndex. "
                "Ensure your CSV has a Date/Datetime column or a datetime-like first column."
            )

    df = df.sort_index()

    # Standardize column names
    df.columns = [flatten_colname(c) for c in df.columns]

    # Coerce to numeric
    df = safe_to_numeric(df)

    return df


def basic_summary(df: pd.DataFrame) -> Dict:
    return {
        "n_rows": int(df.shape[0]),
        "n_cols": int(df.shape[1]),
        "columns": list(df.columns),
        "date_start": str(df.index.min()) if len(df) else None,
        "date_end": str(df.index.max()) if len(df) else None,
        "freq_guess": guess_time_freq(df.index),
    }


def missingness(df: pd.DataFrame) -> pd.DataFrame:
    return (
        pd.DataFrame(
            {
                "missing_count": df.isna().sum(),
                "missing_ratio": (df.isna().mean()).round(6),
            }
        )
        .sort_values("missing_ratio", ascending=False)
    )


def descriptive_stats(df: pd.DataFrame) -> pd.DataFrame:
    stats = df.describe(percentiles=[0.01, 0.05, 0.5, 0.95, 0.99]).T
    stats["skew"] = df.skew(numeric_only=True)
    stats["kurtosis"] = df.kurtosis(numeric_only=True)
    return stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, required=True, help="CSV path")
    parser.add_argument("--out_dir", type=str, required=True, help="Output folder")
    parser.add_argument("--max_rows_preview", type=int, default=5)
    args = parser.parse_args()

    if not os.path.exists(args.input):
        raise FileNotFoundError(f"Input file not found: {args.input}")

    ensure_dir(args.out_dir)

    df = load_timeseries_csv(args.input)

    summary = basic_summary(df)
    miss = missingness(df)
    stats = descriptive_stats(df)

    # Save artifacts
    miss_path = os.path.join(args.out_dir, "missingness.csv")
    stats_path = os.path.join(args.out_dir, "stats.csv")
    report_path = os.path.join(args.out_dir, "report.json")

    miss.to_csv(miss_path)
    stats.to_csv(stats_path)

    report = {
        "input": os.path.abspath(args.input),
        "summary": summary,
        "missing_top5": miss.head(5).to_dict(orient="index"),
        "notes": [
            "This script intentionally keeps only Layer 1 (structure) and Layer 2 (descriptive statistics).",
            "No derived features, correlation, or plots are generated in this version.",
        ],
    }
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    # Console preview
    print(f"[OK] Loaded: {args.input}")
    print(f"[OK] Output folder: {args.out_dir}")
    print(f"[OK] Saved: {miss_path}")
    print(f"[OK] Saved: {stats_path}")
    print(f"[OK] Saved: {report_path}")
    print(
        f"Range: {df.index.min().date()} -> {df.index.max().date()} | "
        f"Rows: {len(df)} | Freq guess: {summary['freq_guess']}"
    )
    print(f"Columns ({len(df.columns)}): {list(df.columns)}")

    print("\n[Preview head]")
    print(df.head(args.max_rows_preview))
    print("\n[Preview tail]")
    print(df.tail(args.max_rows_preview))
    print("\n[Missingness top 5]")
    print(miss.head(5))


if __name__ == "__main__":
    main()