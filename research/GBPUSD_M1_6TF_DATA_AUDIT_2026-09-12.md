# GBPUSD M1 → Six-Timeframe Data Audit

Date: 2026-09-12

## Source
- `GBPUSD_M1_MASTER_2016_2026_V1.zip`
- Master CSV rows after timestamp de-duplication: **3,908,322**
- Range: **2016-01-03 17:00 UTC → 2026-06-30 23:59 UTC**
- OHLC missing rows in the supplied validation summary: **0**
- M1 gaps > 1 minute: **5,621**
- Largest observed gap: **4,326 minutes**

## Volume
The dataset includes `volume_available`. It must not be treated as zero when unavailable.

- M1 volume availability: **61.92%**
- M1 volume-unavailable rows: **38.08%**
- Open interest: unavailable in this dataset → neutral/unknown in the engine.

## Causal six-timeframe construction
The independent engine will build:

`M1 → 5m → 15m → 30m → 1H → 4H → 1D`

No forward-fill of market observations is allowed. For aggregated volume, a timeframe bar is considered volume-known only when all source rows in that aggregate have usable volume; otherwise volume is kept unknown (`NaN`).

| TF | Rows | Volume-known bars | Volume availability |
|---|---:|---:|---:|
| 5m | 783,498 | 484,920 | 61.89% |
| 15m | 261,661 | 161,997 | 61.91% |
| 30m | 131,099 | 81,170 | 61.92% |
| 1H | 65,814 | 40,754 | 61.92% |
| 4H | 16,874 | 10,442 | 61.88% |
| 1D | 3,270 | 2,022 | 61.83% |

## Research split
The first research protocol is fixed chronologically:

- **Train:** 2016–2021
- **Validation:** 2022–2023
- **OOS:** 2024–2025
- **Future holdout:** 2026 (through the dataset end) — not used for tuning

## Important data-quality rule
The 5,621 M1 gaps include normal market/session discontinuities as well as larger gaps. They must not be filled synthetically. Any backtest must operate only on bars actually present and must not create artificial candles across a gap.

## Implementation change
`src/data_loader.py` was updated so `volume_available` is preserved and unavailable volume is not converted to zero during six-timeframe resampling.

Commit: `f1c3502068ae2961cd241e49e1d575780ac54872`

## Next stage
Run the independent engine on the genuine M1-derived six-timeframe data, then report BUY/SELL/WAIT counts and event-driven performance (trade count, win rate, profit factor, expectancy, max drawdown, costs/slippage) separately for Train / Validation / OOS / 2026 holdout. No parameter tuning is permitted on OOS or 2026 holdout.
