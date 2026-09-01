import numpy as np


class TaxSpecialistAgent:
    """Evaluates tax-efficient execution and identifies Tax-Loss Harvesting opportunities."""

    def __init__(self, stcg_rate: float = 0.15, ltcg_rate: float = 0.10):
        self.stcg_rate = stcg_rate
        self.ltcg_rate = ltcg_rate

    def evaluate_tax_impact(
        self, proposed_trades: dict, tax_lots: list, current_prices: dict
    ) -> dict:
        total_tax_liability = 0.0
        harvestable_losses = 0.0

        for asset, trade_val in proposed_trades.items():
            if trade_val < 0:  # Selling asset
                # Simplified linear gain estimate
                estimated_gain = abs(trade_val) * 0.12

                if estimated_gain < 0:
                    harvestable_losses += abs(estimated_gain)
                else:
                    total_tax_liability += estimated_gain * self.stcg_rate

        total_trade_volume = sum(map(abs, proposed_trades.values()))
        tax_efficiency_score = 1.0 - (
            total_tax_liability / (total_trade_volume + 1e-6)
        )

        return {
            "estimated_tax_liability": total_tax_liability,
            "harvestable_losses_identified": harvestable_losses,
            "tax_efficiency_score": tax_efficiency_score,
        }