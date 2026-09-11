"""Rule-based candlestick confirmations inspired by Steve Nison's approach."""
import pandas as pd


def patterns(df):
    o,h,l,c = [pd.to_numeric(df[x], errors="coerce") for x in ("open","high","low","close")]
    body=(c-o).abs(); rng=(h-l).replace(0, pd.NA)
    upper=h-pd.concat([o,c],axis=1).max(axis=1)
    lower=pd.concat([o,c],axis=1).min(axis=1)-l
    out=pd.DataFrame(index=df.index)
    out["hammer"]=(lower >= body*2) & (upper <= body) & (body/rng <= .4)
    out["shooting_star"]=(upper >= body*2) & (lower <= body) & (body/rng <= .4)
    prev_o=o.shift(1); prev_c=c.shift(1)
    out["bullish_engulfing"]=(c>o)&(prev_c<prev_o)&(o<=prev_c)&(c>=prev_o)
    out["bearish_engulfing"]=(c<o)&(prev_c>prev_o)&(o>=prev_c)&(c<=prev_o)
    return out.fillna(False)


def nison_score(df):
    p=patterns(df).iloc[-1]
    score=0
    if p.hammer or p.bullish_engulfing: score += 1
    if p.shooting_star or p.bearish_engulfing: score -= 1
    return score
