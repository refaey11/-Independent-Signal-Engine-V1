# Independent Signal Engine V1

Standalone trading signal engine. This repository is completely independent from the main AI Trading Assistant / Decision Brain project.

## Scope
- Six timeframes: 5m, 15m, 30m, 1H, 4H, 1D
- Steve Nison candlestick confirmation
- Market structure
- Support / resistance
- Pivot sequence
- Trendline / geometry context
- RSI, DMI/ADX, Parabolic SAR, OBV
- Optional volume and open interest when available
- Multi-timeframe confluence
- BUY / SELL / WAIT quality gate
- ATR-based stop-loss / take-profit framework
- Historical backtesting and walk-forward evaluation

## Explicit exclusions
- No Murphy dependency
- No Trading in the Zone dependency
- No Similarity Engine dependency
- No main Decision Brain dependency

## Research standard
No promise of an 80% win rate. Performance must be established by historical testing, costs/slippage, sufficient trade count, walk-forward validation and out-of-sample testing without lookahead or leakage.

## Status
V1 foundation. Implementation will be added incrementally with tests and evidence.
