"""Dependency-free Parabolic SAR implementation."""
import numpy as np


def psar(df, step=0.02, max_af=0.2):
    h = np.asarray(df["high"], dtype=float)
    l = np.asarray(df["low"], dtype=float)
    n = len(df)
    out = np.full(n, np.nan)
    if n < 2:
        return out
    bull = True
    af = step
    ep = h[0]
    out[0] = l[0]
    for i in range(1, n):
        prev = out[i-1]
        sar = prev + af * (ep - prev)
        if bull:
            sar = min(sar, l[i-1], l[i-2] if i >= 2 else l[i-1])
            if l[i] < sar:
                bull, sar, ep, af = False, ep, l[i], step
            elif h[i] > ep:
                ep = h[i]; af = min(max_af, af + step)
        else:
            sar = max(sar, h[i-1], h[i-2] if i >= 2 else h[i-1])
            if h[i] > sar:
                bull, sar, ep, af = True, ep, h[i], step
            elif l[i] < ep:
                ep = l[i]; af = min(max_af, af + step)
        out[i] = sar
    return out


def psar_score(df):
    s = psar(df)
    if len(s) == 0 or np.isnan(s[-1]):
        return 0
    c = float(df["close"].iloc[-1])
    return 1 if c > s[-1] else -1 if c < s[-1] else 0
