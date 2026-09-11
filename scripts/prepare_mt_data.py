"""Prepare local yearly OHLC/M1 files for the independent signal engine.

This utility intentionally accepts local files only. It never downloads or
modifies the source datasets. It concatenates yearly CSVs, normalizes the
schema, removes duplicate timestamps, sorts chronologically, and writes one
canonical CSV that can be passed to the research runner.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.data_loader import normalize_ohlc


def prepare(inputs: list[str], output: str) -> int:
    frames = []
    for item in inputs:
        for path in sorted(Path().glob(item)):
            if path.is_file():
                frames.append(normalize_ohlc(pd.read_csv(path)))

    if not frames:
        raise FileNotFoundError("No input CSV files matched")

    data = pd.concat(frames, axis=0)
    data = data[~data.index.duplicated(keep="first")].sort_index()
    out = Path(output)
    out.parent.mkdir(parents=True, exist_ok=True)
    result = data.reset_index(names="timestamp")
    result.to_csv(out, index=False)
    print(f"Prepared {len(result):,} rows from {len(frames)} files -> {out}")
    print(f"Range: {result['timestamp'].min()} -> {result['timestamp'].max()}")
    return len(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+", help="CSV paths or glob patterns")
    parser.add_argument("--output", default="data/market_master.csv")
    args = parser.parse_args()
    prepare(args.inputs, args.output)
