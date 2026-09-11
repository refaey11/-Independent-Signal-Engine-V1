"""Run chronological train/validation/OOS research on a local OHLC CSV."""
from __future__ import annotations

import argparse
import json
from src.data_loader import load_csv
from src.research_report import run_research


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv")
    parser.add_argument("--warmup", type=int, default=60)
    parser.add_argument("--fee-bps", type=float, default=5.0)
    parser.add_argument("--output", default="research_report.json")
    args = parser.parse_args()
    result = run_research(load_csv(args.csv), warmup=args.warmup, fee_bps=args.fee_bps)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, default=str)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
