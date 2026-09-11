"""Volume/open-interest confirmation. Missing data is UNKNOWN, never zero."""
import pandas as pd


def volume_score(df, lookback=20):
    if "volume" not in df.columns:
        return 0
    v = pd.to_numeric(df["volume"], errors="coerce")
    c = pd.to_numeric(df["close"], errors="coerce")
    if v.dropna().empty or len(df) < lookback + 2:
        return 0
    baseline = v.iloc[-lookback-1:-1].mean()
    if not baseline or pd.isna(baseline):
        return 0
    direction = 1 if c.iloc[-1] > c.iloc[-2] else -1 if c.iloc[-1] < c.iloc[-2] else 0
    expansion = v.iloc[-1] >= 1.2 * baseline
    return direction if expansion else 0


def open_interest_score(df):
    if "open_interest" not in df.columns:
        return 0
    oi = pd.to_numeric(df["open_interest"], errors="coerce")
    c = pd.to_numeric(df["close"], errors="coerce")
    if oi.dropna().size < 2:
        return 0
    d_oi, d_c = oi.iloc[-1] - oi.iloc[-2], c.iloc[-1] - c.iloc[-2]
    if d_oi > 0 and d_c > 0: return 1
    if d_oi > 0 and d_c < 0: return -1
    return 0
