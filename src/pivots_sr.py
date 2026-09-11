"""Causal pivot-sequence and support/resistance context."""


def pivot_levels(df):
    """Classic pivot levels from the latest completed bar."""
    r = df.iloc[-1]
    p = (float(r.high) + float(r.low) + float(r.close)) / 3.0
    return {"pivot": p, "r1": 2*p-float(r.low), "s1": 2*p-float(r.high), "r2": p+(float(r.high)-float(r.low)), "s2": p-(float(r.high)-float(r.low))}


def pivot_score(df):
    """Score price versus the latest pivot and the prior pivot direction."""
    if len(df) < 5:
        return 0
    pivots = (df["high"].astype(float) + df["low"].astype(float) + df["close"].astype(float)) / 3.0
    p0, p1 = float(pivots.iloc[-1]), float(pivots.iloc[-2])
    price = float(df["close"].iloc[-1])
    if price > p0 and p0 >= p1:
        return 1
    if price < p0 and p0 <= p1:
        return -1
    return 0


def sr_score(df, lookback=20):
    """Causal support/resistance breakout context from prior completed bars only.

    A breakout above the prior rolling high is bullish; a break below the prior
    rolling low is bearish. Otherwise the level is neutral. This avoids the
    previous implementation's systematic short bias near nearby historical lows.
    """
    if len(df) < lookback + 1:
        return 0
    price = float(df["close"].iloc[-1])
    resistance = float(df["high"].iloc[-lookback-1:-1].max())
    support = float(df["low"].iloc[-lookback-1:-1].min())
    if price > resistance:
        return 1
    if price < support:
        return -1
    return 0
