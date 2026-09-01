"""TWAP execution algo for Hyperliquid."""
from __future__ import annotations
from typing import Any
from hyperliquid_bot.strategy_base import Strategy
from hyperliquid_bot.types import OrderIntent, Side, Signal

class StrategyImpl(Strategy):
    name = "twap"
    description = "Time-sliced order execution"

    def on_tick(self, market: dict[str, Any]) -> Signal:
        slices = int(self.config.params.get("slices", 10))
        done = self._state.get("slice_idx", 0)
        if done >= slices:
            return Signal("flat", 1.0, "TWAP complete")
        return Signal("long" if self.config.params.get("side", "buy") == "buy" else "short", 0.9, f"slice {done+1}/{slices}")

    def build_orders(self, signal: Signal, market: dict[str, Any]) -> list[OrderIntent]:
        if signal.action not in ("long", "short"):
            return []
        slices = int(self.config.params.get("slices", 10))
        total = float(self.config.params.get("total_size", self.config.size))
        sz = total / slices
        side = Side.BUY if signal.action == "long" else Side.SELL
        self._state["slice_idx"] = self._state.get("slice_idx", 0) + 1
        return [OrderIntent(self.config.coin, side, sz, market["mid"], tag=f"twap_{self._state['slice_idx']}")]
