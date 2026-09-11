"""Independent confluence signal engine. BUY/SELL are gated; otherwise WAIT."""
from .indicators import rsi, atr, adx
from .candles_nison import nison_score
from .market_structure import structure_score
from .pivots_sr import sr_score


def generate_signal(df, weights=None, buy_threshold=70, sell_threshold=-70):
    weights=weights or {"nison":20,"structure":15,"sr":15,"momentum":20,"trend":10,"volume":10,"mtf":10}
    score=0
    score += nison_score(df)*weights["nison"]
    score += structure_score(df)*weights["structure"]
    score += sr_score(df)*weights["sr"]
    rv=float(rsi(df).iloc[-1]); score += (1 if rv>55 else -1 if rv<45 else 0)*weights["momentum"]
    av=float(adx(df).iloc[-1,] if False else adx(df)[0].iloc[-1]); score += (1 if av>=20 and structure_score(df)>0 else -1 if av>=20 and structure_score(df)<0 else 0)*weights["trend"]
    signal="BUY" if score>=buy_threshold else "SELL" if score<=sell_threshold else "WAIT"
    a=float(atr(df).iloc[-1]); price=float(df.close.iloc[-1])
    return {"signal":signal,"score":score,"close":price,"atr":a,"sl":price-1.5*a if signal=="BUY" else price+1.5*a if signal=="SELL" else None,"tp":price+3*a if signal=="BUY" else price-3*a if signal=="SELL" else None}
