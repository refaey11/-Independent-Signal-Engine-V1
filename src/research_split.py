"""Chronological dataset splitting for unbiased signal-engine research."""
from __future__ import annotations

from typing import Tuple
import pandas as pd


def chronological_split(
    df: pd.DataFrame,
    train_ratio: float = 0.60,
    validation_ratio: float = 0.20,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split chronologically into train, validation and untouched OOS data.

    No shuffling is performed. The OOS segment is always the final segment.
    """
    if not 0 < train_ratio < 1:
        raise ValueError("train_ratio must be between 0 and 1")
    if not 0 < validation_ratio < 1:
        raise ValueError("validation_ratio must be between 0 and 1")
    if train_ratio + validation_ratio >= 1:
        raise ValueError("train_ratio + validation_ratio must be below 1")
    if len(df) < 10:
        raise ValueError("At least 10 rows are required for a research split")

    data = df.sort_index().copy()
    n = len(data)
    train_end = int(n * train_ratio)
    validation_end = int(n * (train_ratio + validation_ratio))
    train = data.iloc[:train_end].copy()
    validation = data.iloc[train_end:validation_end].copy()
    oos = data.iloc[validation_end:].copy()
    return train, validation, oos
