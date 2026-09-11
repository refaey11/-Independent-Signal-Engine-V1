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


def sr_score(df, tolerance=0.002):
    """Causal support/resistance proximity score from prior bars only."""
    if len(df) < 10:
        return 0
    price = float(df.close.iloc[-1])
    levels = []
    for i in range(max(0, len(df)-50), len(df)-1):
        levels += [float(df.high.iloc[i]), float(df.low.iloc[i])]
    near = [x for x in levels if abs(x-price)/price <= tolerance]
    if not near:
        return 0
    return 1 if price >= max(near) else -1
