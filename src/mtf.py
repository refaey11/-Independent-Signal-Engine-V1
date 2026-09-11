"""Multi-timeframe confluence. Inputs are already-resampled OHLCV frames."""
from .market_structure import structure_score
from .trend_geometry import trend_geometry_score

TIMEFRAMES = ["5m", "15m", "30m", "1H", "4H", "1D"]


def mtf_score(frames):
    scores = {}
    for tf in TIMEFRAMES:
        df = frames.get(tf)
        if df is None or len(df) < 20:
            scores[tf] = 0
            continue
        scores[tf] = structure_score(df) + trend_geometry_score(df)
    usable = [v for v in scores.values() if v]
    if not usable:
        return 0, scores
    total = sum(usable)
    return (1 if total > 0 else -1 if total < 0 else 0), scores
