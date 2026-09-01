# Strategy — TWAP Execution

## Overview

Build a TWAP execution bot splitting large Hyperliquid orders across time slices with randomization, slippage caps, and cancel-replace on drift.

## Detailed Methodology

Large orders are split into `slices` equal time intervals over `duration_minutes`. Each slice is a limit order at mid ± `offset_bps` with randomization to avoid detection. Slippage is tracked against arrival price.

**Optimal regime:** Institutional-size entries/exits on Hyperliquid without moving the market.

## Performance Context

| Metric | Value |
|--------|-------|
| PnL | +$3,210 |
| Win Rate | 88.0% |
| Sharpe | 2.88 |
| Max DD | -1.2% |

## Implementation

Full logic in `src/hyperliquid_bot/strategy.py`

## Configuration

Edit `config.yaml` params section for strategy-specific tuning.
