import numpy as np
import pandas as pd

from src.backtest import run_backtest


def test_backtest_reports_directional_metrics_and_uses_mtf_path():
    idx = pd.date_range("2024-01-01", periods=180, freq="5min", tz="UTC")
    close = 100 + np.cumsum(np.full(len(idx), 0.05))
    df = pd.DataFrame({
        "open": close - 0.02,
        "high": close + 0.10,
        "low": close - 0.10,
        "close": close,
        "volume": np.full(len(idx), 1000.0),
    }, index=idx)
    out = run_backtest(df, warmup=60, fee_bps=5)
    assert "expectancy" in out
    assert "avg_win" in out
    assert "avg_loss" in out
    assert "buy_count" in out
    assert "sell_count" in out
    assert out["trade_count"] >= 0
