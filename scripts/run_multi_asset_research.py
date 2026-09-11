"""Run the same chronological research protocol across local asset CSVs."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.data_loader import load_csv
from src.research_report import run_research


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", help="Asset CSV files")
    parser.add_argument("--output", default="research_multi_asset.json")
    parser.add_argument("--fee-bps", type=float, default=5.0)
    parser.add_argument("--warmup", type=int, default=60)
    args = parser.parse_args()

    report = {}
    for file_name in args.files:
        path = Path(file_name)
        data = load_csv(path)
        report[path.stem] = run_research(data, warmup=args.warmup, fee_bps=args.fee_bps)

    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, default=str)
    print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    main()
