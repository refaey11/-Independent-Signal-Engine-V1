import pandas as pd
import pytest

from src.research_split import chronological_split


def test_split_is_chronological_and_disjoint():
    idx = pd.date_range("2020-01-01", periods=100, freq="h", tz="UTC")
    df = pd.DataFrame({"close": range(100)}, index=idx)
    train, validation, oos = chronological_split(df)
    assert len(train) == 60
    assert len(validation) == 20
    assert len(oos) == 20
    assert train.index.max() < validation.index.min()
    assert validation.index.max() < oos.index.min()
    assert train["close"].iloc[-1] == 59
    assert oos["close"].iloc[0] == 80


def test_split_rejects_invalid_ratios():
    df = pd.DataFrame({"close": range(20)})
    with pytest.raises(ValueError):
        chronological_split(df, train_ratio=0.8, validation_ratio=0.3)
