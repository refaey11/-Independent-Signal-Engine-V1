"""Contextual signal gate: regime first, Nison as trigger, confluence required."""


def gate_signal(components):
    """Return BUY/SELL/WAIT without allowing a candle pattern to set direction alone.

    Regime votes come from trend, structure and geometry. A Nison candle must
    agree with the regime, and momentum must confirm it. This is deliberately
    conservative and is not tuned on OOS data.
    """
    trend = int(components.get("trend", 0))
    structure = int(components.get("structure", 0))
    geometry = int(components.get("geometry", 0))
    momentum = int(components.get("momentum", 0))
    nison = int(components.get("nison", 0))

    regime_votes = trend + structure + geometry
    if regime_votes >= 2:
        direction = 1
    elif regime_votes <= -2:
        direction = -1
    else:
        return "WAIT"

    # Nison is a trigger/confirmation, never the standalone direction source.
    if nison != direction or momentum != direction:
        return "WAIT"

    return "BUY" if direction == 1 else "SELL"
