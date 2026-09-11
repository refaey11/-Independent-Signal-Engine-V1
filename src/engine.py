"""Independent multi-factor signal engine. BUY/SELL are context-gated; otherwise WAIT."""
from .indicators import rsi, atr, adx
from .candles_nison import nison_score
from .market_structure import structure_score
from .pivots_sr import sr_score, pivot_score
from .volume_flow import volume_score, open_interest_score
from .trend_geometry import trend_geometry_score
from .parabolic_sar import psar_score
from .mtf import mtf_score
from .signal_gate import gate_signal

DEFAULT_WEIGHTS = {
    "nison": 20, "structure": 15, "sr": 15, "pivot": 10,
    "momentum": 10, "trend": 10, "volume": 5, "geometry": 5,
    "sar": 5, "mtf": 5,
}


def _quality(score, signal, buy_threshold, sell_threshold):
    strength = abs(float(score))
    active = max(abs(float(buy_threshold)), abs(float(sell_threshold)))
    if signal == "WAIT":
        return "C"
    if strength >= 90:
        return "A+"
    if strength >= max(80, active):
        return "A"
    return "B"


def generate_signal(df, frames=None, weights=None, buy_threshold=70, sell_threshold=-70, sl_atr=1.5, tp_atr=3.0):
    w = {**DEFAULT_WEIGHTS, **(weights or {})}
    components = {}
    components["nison"] = nison_score(df)
    components["structure"] = structure_score(df)
    components["sr"] = sr_score(df)
    components["pivot"] = pivot_score(df)
    rv = float(rsi(df).iloc[-1])
    components["momentum"] = 1 if rv > 55 else -1 if rv < 45 else 0
    av, pdi, mdi = adx(df)
    adx_v = float(av.iloc[-1])
    components["trend"] = 1 if adx_v >= 20 and float(pdi.iloc[-1]) > float(mdi.iloc[-1]) else -1 if adx_v >= 20 and float(mdi.iloc[-1]) > float(pdi.iloc[-1]) else 0
    components["volume"] = volume_score(df)
    components["geometry"] = trend_geometry_score(df)
    components["sar"] = psar_score(df)
    mtf_direction, mtf_detail = mtf_score(frames or {})
    components["mtf"] = mtf_direction
    score = sum(components[k] * w[k] for k in components)

    # The contextual gate is the hard directional decision. A large additive
    # score cannot override a missing regime or Nison/momentum confirmation.
    signal = gate_signal(components)
    quality = _quality(score, signal, buy_threshold, sell_threshold)
    a = float(atr(df).iloc[-1]); price = float(df.close.iloc[-1])
    return {
        "signal": signal, "quality": quality, "score": score,
        "components": components, "mtf": mtf_detail,
        "open_interest_score": open_interest_score(df), "close": price, "atr": a,
        "sl": price - sl_atr*a if signal == "BUY" else price + sl_atr*a if signal == "SELL" else None,
        "tp": price + tp_atr*a if signal == "BUY" else price - tp_atr*a if signal == "SELL" else None,
    }
