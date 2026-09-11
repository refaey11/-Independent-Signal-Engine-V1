"""Download public Binance spot klines into the CSV format used by the engine."""
from __future__ import annotations

import argparse
import time
from datetime import datetime, timezone

import pandas as pd
import requests

URL = "https://api.binance.com/api/v3/klines"
COLUMNS = ["timestamp", "open", "high", "low", "close", "volume", "close_time", "quote_volume", "trades", "taker_buy_volume", "taker_buy_quote_volume", "ignore"]


def ms(value: str) -> int:
    return int(datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=timezone.utc).timestamp() * 1000)


def download(symbol: str, interval: str, start: str, end: str, output: str) -> None:
    start_ms, end_ms = ms(start), ms(end)
    rows = []
    cursor = start_ms
    session = requests.Session()
    while cursor < end_ms:
        params = {"symbol": symbol.upper(), "interval": interval, "startTime": cursor, "endTime": end_ms, "limit": 1000}
        response = session.get(URL, params=params, timeout=30)
        response.raise_for_status()
        batch = response.json()
        if not batch:
            break
        rows.extend(batch)
        next_cursor = int(batch[-1][0]) + 1
        if next_cursor <= cursor:
            break
        cursor = next_cursor
        time.sleep(0.15)

    if not rows:
        raise RuntimeError("No Binance klines returned for the requested range")
    df = pd.DataFrame(rows, columns=COLUMNS)
    df = df.drop_duplicates(subset=["timestamp"]).sort_values("timestamp")
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].apply(pd.to_numeric)
    df[["timestamp", "open", "high", "low", "close", "volume"]].to_csv(output, index=False)
    print(f"Wrote {len(df)} rows to {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", default="BTCUSDT")
    parser.add_argument("--interval", default="5m")
    parser.add_argument("--start", required=True, help="ISO-8601 UTC, e.g. 2024-01-01T00:00:00Z")
    parser.add_argument("--end", required=True, help="ISO-8601 UTC")
    parser.add_argument("--output", default="data/btcusdt_5m.csv")
    args = parser.parse_args()
    download(args.symbol, args.interval, args.start, args.end, args.output)
