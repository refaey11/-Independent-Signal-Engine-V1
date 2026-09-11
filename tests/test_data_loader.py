import pandas as pd
import pytest

from src.data_loader import build_timeframes, normalize_ohlc


def sample():
    idx = pd.date_range("2024-01-01", periods=120, freq="5min", tz="UTC")
    close = pd.Series(range(100, 220), index=idx, dtype=float)
    return pd.DataFrame({
        "timestamp": idx,
        "open": close.values - 0.5,
        "high": close.values + 1,
        "low": close.values - 1,
        "close": close.values,
        "volume": 10,
    })


def test_normalize_keeps_missing_volume_and_oi_unknown():
    df = sample().drop(columns=["volume"])
    out = normalize_ohlc(df)
    assert out["volume"].isna().all()
    assert out["open_interest"].isna().all()


def test_normalize_rejects_missing_ohlc():
    df = sample().drop(columns=["low"])
    with pytest.raises(ValueError):
        normalize_ohlc(df)


def test_builds_six_timeframes_without_future_fill():
    frames = build_timeframes(sample())
    assert list(frames) == ["5m", "15m", "30m", "1H", "4H", "1D"]
    assert len(frames["15m"]) > 0
    assert frames["15m"].index.is_monotonic_increasing
    assert frames["15m"]["open_interest"].isna().all()
