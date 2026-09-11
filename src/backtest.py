"""Simple no-lookahead close-to-close backtest for the signal engine."""
import pandas as pd
from .engine import generate_signal


def run_backtest(df, warmup=60, fee_bps=5):
    trades = []
    equity = 1.0
    peak = equity
    max_dd = 0.0
    for i in range(warmup, len(df) - 1):
        history = df.iloc[:i+1]
        out = generate_signal(history)
        side = out["signal"]
        if side == "WAIT":
            continue
        entry = float(df["close"].iloc[i])
        exit_price = float(df["close"].iloc[i+1])
        raw = (exit_price / entry - 1.0) if side == "BUY" else (entry / exit_price - 1.0)
        net = raw - 2 * fee_bps / 10000.0
        equity *= 1 + net
        peak = max(peak, equity)
        max_dd = max(max_dd, 1 - equity / peak)
        trades.append({"index": df.index[i], "side": side, "entry": entry, "exit": exit_price, "return": net, "equity": equity})
    t = pd.DataFrame(trades)
    if t.empty:
        return {"trades": t, "trade_count": 0, "win_rate": 0.0, "profit_factor": 0.0, "max_drawdown": 0.0, "equity": equity}
    wins = t[t["return"] > 0]["return"]
    losses = -t[t["return"] < 0]["return"]
    pf = float(wins.sum() / losses.sum()) if losses.sum() else float("inf")
    return {"trades": t, "trade_count": len(t), "win_rate": float((t["return"] > 0).mean()), "profit_factor": pf, "max_drawdown": float(max_dd), "equity": float(equity)}
