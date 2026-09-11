"""Data loading and causal six-timeframe preparation for the independent signal engine."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable

import pandas as pd

BASE_COLUMNS = ["open", "high", "low", "close"]
OPTIONAL_COLUMNS = ["volume", "open_interest"]
TIMEFRAMES = ["5m", "15m", "30m", "1H", "4H", "1D"]
_RULES = {"5m": "5min", "15m": "15min", "30m": "30min", "1H": "1h", "4H": "4h", "1D": "1D"}


def load_csv(path: str | Path) -> pd.DataFrame:
    """Load, normalize, validate and chronologically sort OHLC data from CSV."""
    return normalize_ohlc(pd.read_csv(path))


def normalize_ohlc(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize common column names and validate an OHLC time series.

    Missing volume/open-interest stay NaN and are never interpreted as zero.
    """
    out = df.copy()
    out = out.rename(columns={c: c.strip().lower().replace(" ", "_") for c in out.columns})
    aliases = {
        "datetime": "timestamp", "date": "timestamp", "time": "timestamp",
        "open_price": "open", "high_price": "high", "low_price": "low", "close_price": "close",
        "tick_volume": "volume", "openinterest": "open_interest", "oi": "open_interest",
    }
    out = out.rename(columns={k: v for k, v in aliases.items() if k in out.columns})

    if "timestamp" in out.columns:
        out["timestamp"] = pd.to_datetime(out["timestamp"], utc=True, errors="coerce")
        out = out.dropna(subset=["timestamp"]).set_index("timestamp")
    elif not isinstance(out.index, pd.DatetimeIndex):
        raise ValueError("CSV must contain timestamp/datetime/date/time or a DatetimeIndex")
    else:
        out.index = pd.to_datetime(out.index, utc=True, errors="coerce")
        out = out[~out.index.isna()]

    missing = [c for c in BASE_COLUMNS if c not in out.columns]
    if missing:
        raise ValueError(f"Missing required OHLC columns: {missing}")

    for col in BASE_COLUMNS + OPTIONAL_COLUMNS:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")

    out = out.sort_index()
    out = out[~out.index.duplicated(keep="last")]
    out = out.dropna(subset=BASE_COLUMNS)
    for col in OPTIONAL_COLUMNS:
        if col not in out.columns:
            out[col] = float("nan")
    return out


def resample_ohlcv(df: pd.DataFrame, rule: str) -> pd.DataFrame:
    """Resample OHLCV/OI without forward-filling market observations."""
    df = normalize_ohlc(df)
    pandas_rule = _RULES.get(rule, rule)
    agg = {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum", "open_interest": "last"}
    out = df.resample(pandas_rule, label="right", closed="right").agg(agg)
    return out.dropna(subset=BASE_COLUMNS)


def build_timeframes(df: pd.DataFrame, timeframes: Iterable[str] = TIMEFRAMES) -> Dict[str, pd.DataFrame]:
    """Build requested timeframes from one base series."""
    base = normalize_ohlc(df)
    return {tf: resample_ohlcv(base, tf) for tf in timeframes}
