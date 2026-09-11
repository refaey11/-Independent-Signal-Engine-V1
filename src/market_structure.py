"""Simple non-lookahead structure context."""

def structure_score(df, lookback=5):
    if len(df) < lookback + 1: return 0
    closes=df["close"]
    recent=closes.iloc[-lookback:]
    prior=closes.iloc[-2*lookback:-lookback] if len(closes)>=2*lookback else closes.iloc[:-lookback]
    if len(prior)==0: return 0
    if recent.mean()>prior.mean() and recent.iloc[-1]>recent.iloc[0]: return 1
    if recent.mean()<prior.mean() and recent.iloc[-1]<recent.iloc[0]: return -1
    return 0
