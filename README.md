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

## Data ingestion
The project does **not** require market data to live in Git history. Keep large M1 datasets outside Git and prepare them locally before research.

Known source data includes MetaTrader-style M1 files such as `DAT_MT_EURUSD_M1_2016.csv` and the Dropbox master archive `EURUSD_M1_MASTER_2016_2026_V1.zip`.

For yearly/local CSV files:

```bash
python scripts/prepare_mt_data.py "data/EURUSD/*.csv" --output data/EURUSD_M1_master.csv
python scripts/run_research.py data/EURUSD_M1_master.csv --output research_EURUSD.json
```

For multiple assets after preparing canonical CSVs:

```bash
python scripts/run_multi_asset_research.py data/EURUSD.csv data/GBPUSD.csv data/XAUUSD.csv data/USDJPY.csv --output research_multi_asset.json
```

The runner preserves causal history across train/validation/OOS boundaries. It does not tune on OOS data.

## Research standard
No promise of an 80% win rate. Performance must be established by historical testing, costs/slippage, sufficient trade count, walk-forward validation and out-of-sample testing without lookahead or leakage.

## Current status
- Code foundation implemented.
- Six-timeframe pipeline implemented.
- Historical research runner implemented.
- CI is green after the latest causal-test fix.
- Real-market performance numbers are **not claimed yet** because the large Dropbox source archives still need to be made available to the execution runtime.

## Next evidence gate
The next valid milestone is a real-data run on EURUSD first, followed by GBPUSD, XAUUSD and USDJPY using the exact same protocol. Only then should win rate, profit factor, expectancy and drawdown be judged.
