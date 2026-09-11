"""Core, dependency-light technical indicators."""
import numpy as np
import pandas as pd


def _close(df):
    return pd.to_numeric(df["close"], errors="coerce")


def rsi(df, period=14):
    c = _close(df)
    d = c.diff()
    gain = d.clip(lower=0).ewm(alpha=1 / period, adjust=False).mean()
    loss = (-d.clip(upper=0)).ewm(alpha=1 / period, adjust=False).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def atr(df, period=14):
    h, l, c = [pd.to_numeric(df[x], errors="coerce") for x in ("high", "low", "close")]
    prev = c.shift(1)
    tr = pd.concat([(h-l), (h-prev).abs(), (l-prev).abs()], axis=1).max(axis=1)
    return tr.ewm(alpha=1 / period, adjust=False).mean()


def adx(df, period=14):
    h, l, c = [pd.to_numeric(df[x], errors="coerce") for x in ("high", "low", "close")]
    up = h.diff(); down = -l.diff()
    plus_dm = up.where((up > down) & (up > 0), 0.0)
    minus_dm = down.where((down > up) & (down > 0), 0.0)
    prev = c.shift(1)
    tr = pd.concat([(h-l), (h-prev).abs(), (l-prev).abs()], axis=1).max(axis=1)
    atr_v = tr.ewm(alpha=1 / period, adjust=False).mean()
    plus_di = 100 * plus_dm.ewm(alpha=1 / period, adjust=False).mean() / atr_v
    minus_di = 100 * minus_dm.ewm(alpha=1 / period, adjust=False).mean() / atr_v
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)
    return dx.ewm(alpha=1 / period, adjust=False).mean(), plus_di, minus_di


def obv(df):
    c = _close(df)
    v = pd.to_numeric(df.get("volume", pd.Series(index=df.index, dtype=float)), errors="coerce").fillna(0)
    direction = np.sign(c.diff()).fillna(0)
    return (direction * v).cumsum()
