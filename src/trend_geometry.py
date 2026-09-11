"""Simple causal trend/geometry context using rolling regression slope."""
import numpy as np


def trend_geometry_score(df, lookback=20):
    if len(df) < lookback:
        return 0
    y = np.asarray(df["close"].iloc[-lookback:], dtype=float)
    x = np.arange(lookback, dtype=float)
    slope = np.polyfit(x, y, 1)[0]
    scale = max(abs(y.mean()), 1e-12)
    normalized = slope / scale
    if normalized > 0.0005:
        return 1
    if normalized < -0.0005:
        return -1
    return 0
