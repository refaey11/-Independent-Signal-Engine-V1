import numpy as np
import pandas as pd
from src.engine import generate_signal
from src.backtest import run_backtest


def sample(n=120):
    idx = pd.date_range("2024-01-01", periods=n, freq="5min", tz="UTC")
    close = 100 + np.cumsum(np.linspace(0.02, 0.3, n))
    return pd.DataFrame({"timestamp": idx, "open": close - 0.1, "high": close + 0.3,
                         "low": close - 0.3, "close": close, "volume": np.full(n, 1000.0)})


def test_signal_contract():
    out = generate_signal(sample())
    assert out["signal"] in {"BUY", "SELL", "WAIT"}
    assert isinstance(out["score"], (int, float))


def test_backtest_is_causal():
    result = run_backtest(sample())
    assert "trade_count" in result
    assert "max_drawdown" in result
