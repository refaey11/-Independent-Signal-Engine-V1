"""Run the independent signal engine backtest on a local CSV."""
from __future__ import annotations

import argparse
import json

from src.backtest import run_backtest
from src.data_loader import load_csv


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", help="CSV containing timestamp and OHLC columns")
    parser.add_argument("--warmup", type=int, default=60)
    parser.add_argument("--fee-bps", type=float, default=5.0)
    args = parser.parse_args()

    df = load_csv(args.csv)
    result = run_backtest(df, warmup=args.warmup, fee_bps=args.fee_bps)
    summary = {k: v for k, v in result.items() if k != "trades"}
    print(json.dumps(summary, indent=2, default=str))

    if not result["trades"].empty:
        result["trades"].to_csv("backtest_trades.csv", index=False)
        print("Wrote backtest_trades.csv")


if __name__ == "__main__":
    main()
