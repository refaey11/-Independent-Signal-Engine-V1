"""No-lookahead backtest for the independent signal engine."""
from __future__ import annotations

import pandas as pd

from .data_loader import build_timeframes
from .engine import generate_signal


def _metrics(trades: pd.DataFrame, equity: float, max_dd: float) -> dict:
    if trades.empty:
        return {"trades": trades, "trade_count": 0, "buy_count": 0, "sell_count": 0,
                "win_rate": 0.0, "profit_factor": 0.0, "expectancy": 0.0,
                "avg_win": 0.0, "avg_loss": 0.0, "max_drawdown": float(max_dd), "equity": float(equity)}
    wins = trades.loc[trades["return"] > 0, "return"]
    losses = -trades.loc[trades["return"] < 0, "return"]
    pf = float(wins.sum() / losses.sum()) if losses.sum() else float("inf")
    return {"trades": trades, "trade_count": len(trades),
            "buy_count": int((trades["side"] == "BUY").sum()),
            "sell_count": int((trades["side"] == "SELL").sum()),
            "win_rate": float((trades["return"] > 0).mean()),
            "profit_factor": pf, "expectancy": float(trades["return"].mean()),
            "avg_win": float(wins.mean()) if not wins.empty else 0.0,
            "avg_loss": float(-losses.mean()) if not losses.empty else 0.0,
            "max_drawdown": float(max_dd), "equity": float(equity)}


def run_backtest(df, warmup=60, fee_bps=5, start_index=None, end_index=None):
    """Backtest causally; optional bounds select which trades are counted.

    Full prior history is retained before start_index, so validation/OOS do not
    reset indicator and multi-timeframe context at a split boundary.
    """
    df = df.sort_index().copy()
    start = warmup if start_index is None else max(warmup, int(start_index))
    end = len(df) - 1 if end_index is None else min(int(end_index), len(df) - 1)
    if start >= end:
        return _metrics(pd.DataFrame(), 1.0, 0.0)

    trades = []
    equity = 1.0
    peak = equity
    max_dd = 0.0
    for i in range(start, end):
        history = df.iloc[: i + 1]
        frames = build_timeframes(history)
        out = generate_signal(history, frames=frames)
        side = out["signal"]
        if side == "WAIT":
            continue
        entry = float(df["close"].iloc[i])
        exit_price = float(df["close"].iloc[i + 1])
        raw = (exit_price / entry - 1.0) if side == "BUY" else (entry / exit_price - 1.0)
        net = raw - 2 * fee_bps / 10000.0
        equity *= 1 + net
        peak = max(peak, equity)
        max_dd = max(max_dd, 1 - equity / peak)
        trades.append({"index": df.index[i], "side": side, "score": out["score"],
                       "entry": entry, "exit": exit_price, "return": net, "equity": equity})
    return _metrics(pd.DataFrame(trades), equity, max_dd)
