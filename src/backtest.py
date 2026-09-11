"""No-lookahead event-driven backtest for the independent signal engine."""
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


def _resolve_trade(df, entry_i, side, entry, atr_value, sl_atr, tp_atr, max_hold):
    """Resolve one trade using only bars after entry; same-bar SL/TP is SL."""
    sl = entry - sl_atr * atr_value if side == "BUY" else entry + sl_atr * atr_value
    tp = entry + tp_atr * atr_value if side == "BUY" else entry - tp_atr * atr_value
    last = min(len(df) - 1, entry_i + max_hold)
    for j in range(entry_i + 1, last + 1):
        hi = float(df["high"].iloc[j])
        lo = float(df["low"].iloc[j])
        if side == "BUY":
            hit_sl, hit_tp = lo <= sl, hi >= tp
        else:
            hit_sl, hit_tp = hi >= sl, lo <= tp
        if hit_sl and hit_tp:
            return j, sl, "SL", -sl_atr
        if hit_sl:
            return j, sl, "SL", -sl_atr
        if hit_tp:
            return j, tp, "TP", tp_atr
    exit_price = float(df["close"].iloc[last])
    r_atr = ((exit_price - entry) / atr_value) if side == "BUY" else ((entry - exit_price) / atr_value)
    return last, exit_price, "TIME", r_atr


def run_backtest(
    df,
    warmup=60,
    fee_bps=5,
    start_index=None,
    end_index=None,
    sl_atr=1.5,
    tp_atr=3.0,
    max_hold=24,
):
    """Backtest causally with ATR SL/TP and non-overlapping positions.

    Full prior history is retained before start_index, so validation/OOS do not
    reset indicators and multi-timeframe context at a split boundary.
    A signal is generated at bar close and the position is evaluated from the
    following bar onward. If SL and TP are both touched in one bar, SL wins.
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
    i = start
    while i < end:
        history = df.iloc[: i + 1]
        frames = build_timeframes(history)
        out = generate_signal(history, frames=frames, sl_atr=sl_atr, tp_atr=tp_atr)
        side = out["signal"]
        if side == "WAIT":
            i += 1
            continue

        entry = float(df["close"].iloc[i])
        atr_value = float(out["atr"])
        if not pd.notna(atr_value) or atr_value <= 0:
            i += 1
            continue

        exit_i, exit_price, reason, r_atr = _resolve_trade(
            df, i, side, entry, atr_value, sl_atr, tp_atr, max_hold
        )
        raw = r_atr * atr_value / entry
        net = raw - 2 * fee_bps / 10000.0
        equity *= 1 + net
        peak = max(peak, equity)
        max_dd = max(max_dd, 1 - equity / peak)
        trades.append({
            "index": df.index[i], "side": side, "score": out["score"],
            "quality": out["quality"], "entry": entry, "exit": exit_price,
            "exit_index": df.index[exit_i], "bars_held": exit_i - i,
            "exit_reason": reason, "return": net, "equity": equity,
        })
        i = max(i + 1, exit_i)

    return _metrics(pd.DataFrame(trades), equity, max_dd)
