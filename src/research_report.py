"""Chronological train/validation/OOS evaluation for the independent engine."""
from __future__ import annotations

from dataclasses import dataclass
import pandas as pd

from .backtest import run_backtest


@dataclass(frozen=True)
class ResearchSplit:
    train_end: int
    validation_end: int


def make_split(df: pd.DataFrame, train_ratio: float = 0.60, validation_ratio: float = 0.20) -> ResearchSplit:
    if train_ratio <= 0 or validation_ratio <= 0 or train_ratio + validation_ratio >= 1:
        raise ValueError("train_ratio and validation_ratio must be positive and leave an OOS segment")
    n = len(df)
    if n < 100:
        raise ValueError("At least 100 rows are required")
    return ResearchSplit(int(n * train_ratio), int(n * (train_ratio + validation_ratio)))


def run_research(df: pd.DataFrame, warmup: int = 60, fee_bps: float = 5.0) -> dict:
    """Evaluate chronological segments while preserving full causal history.

    Indicators at validation/OOS timestamps still see all earlier bars; only
    trades whose decision timestamp belongs to the requested segment are counted.
    This avoids the common error of resetting indicator history at split boundaries.
    """
    data = df.sort_index().copy()
    split = make_split(data)
    segments = {
        "train": (warmup, split.train_end),
        "validation": (split.train_end, split.validation_end),
        "oos": (split.validation_end, len(data) - 1),
    }
    report = {"rows": len(data), "split": split.__dict__, "segments": {}}
    for name, (start, end) in segments.items():
        result = run_backtest(data, warmup=warmup, fee_bps=fee_bps, start_index=start, end_index=end)
        report["segments"][name] = {k: v for k, v in result.items() if k != "trades"}
    return report
