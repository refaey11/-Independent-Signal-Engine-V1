# Gate Grid Research — 2026-09-11

## Purpose

Evaluate candidate directional gates for the independent signal engine using the available EURUSD H1 dataset (2016–2025), while keeping Nison as confirmation rather than a standalone direction source.

This is exploratory research only. It does **not** claim an 80% win rate and does not authorize tuning against OOS.

## Dataset limitation

The available dataset is EURUSD H1. It cannot provide genuine 5m/15m/30m information by downsampling. Full six-timeframe validation therefore still requires the M1 master data.

Volume/open-interest are not available in the inspected H1 rows, so they are treated as unknown/neutral rather than zero.

## Protocol

- Train: 2016–2021
- Validation: 2022–2023
- OOS: 2024–2025 (diagnostic only; not used for selection)
- Directional regime candidates are combinations of trend, structure, geometry, S/R, and pivot.
- Nison confirmation is required for the primary candidate tests.
- Momentum was also tested as a confirmation requirement.
- Event-style exits were evaluated with ATR-based SL/TP and a maximum holding period.
- No future bars are used to create a signal.

## Main findings

The previously added simple gate (trend + structure + geometry majority, with Nison + momentum agreement) was not profitable in the proper event-driven OOS test, so it is **not validated**.

The grid search shows a more interesting research direction: geometry appears repeatedly in the better-performing combinations, while blindly requiring every component reduces signal quality and/or trade count.

### Candidate: structure + geometry + S/R, with Nison + momentum confirmation

At SL=1.5 ATR / TP=3 ATR / max hold=24:

| Segment | Trades | Win rate | Mean R/ATR | PF-like |
|---|---:|---:|---:|---:|
| Train 2016–2021 | 459 | 33.55% | -0.1376 | 0.858 |
| Validation 2022–2023 | 166 | 39.16% | +0.1825 | 1.203 |
| OOS 2024–2025 | 170 | 35.88% | +0.0415 | 1.045 |

This is **not sufficient evidence of a robust edge** because the train segment is negative and the OOS margin is small.

### Candidate: geometry + pivot, with Nison + momentum confirmation

At SL=1.5 ATR / TP=3 ATR / max hold=24:

| Segment | Trades | Win rate | Mean R/ATR | PF-like |
|---|---:|---:|---:|---:|
| Train 2016–2021 | 62 | 37.10% | -0.0259 | 0.969 |
| Validation 2022–2023 | 61 | 44.26% | +0.2114 | 1.256 |
| OOS 2024–2025 | 21 | 23.81% | -0.5699 | 0.501 |

This fails robustness because OOS collapses and the trade count is small.

### Candidate: trend + geometry, with Nison + momentum confirmation

At SL=1.5 ATR / TP=3 ATR / max hold=24:

| Segment | Trades | Win rate | Mean R/ATR | PF-like |
|---|---:|---:|---:|---:|
| Train 2016–2021 | 79 | 36.71% | -0.0916 | 0.892 |
| Validation 2022–2023 | 69 | 42.03% | +0.0851 | 1.099 |
| OOS 2024–2025 | 26 | 30.77% | -0.1825 | 0.816 |

Also not robust.

## Important observation about Nison

Removing the Nison confirmation from a gate can increase trade count, but the tested combinations generally became weaker or more noisy. Nison should remain a trigger/confirmation layer, not the directional engine.

## Next research direction

Do **not** promote any current gate to production.

The next controlled experiment should be:

1. Use Train 2016–2021 only to define a small candidate family.
2. Validate those candidates on 2022–2023.
3. Lock the candidate before touching 2024–2025 OOS.
4. Run the same locked logic on the real M1 data so all six timeframes (5m, 15m, 30m, 1H, 4H, 1D) are genuine.
5. Include realistic spread/slippage/fees in price-space returns, not only normalized R/ATR diagnostics.
6. Report trade count, PF, expectancy, win/loss distribution, max drawdown, and performance by year/asset.

## Status

**Research finding: no validated profitable gate yet.**

The engine architecture is improving, but an 80% win-rate claim is currently unsupported by the available evidence.
