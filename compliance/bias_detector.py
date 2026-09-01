import pandas as pd

class BiasDetector:
    """Tests rebalancing decisions for algorithmic bias across risk profiles."""

    @staticmethod
    def detect_bias(rebalance_history_df: pd.DataFrame) -> dict:
        if rebalance_history_df.empty:
            return {"bias_detected": False, "group_rates": {}}

        rates = rebalance_history_df.groupby("risk_profile")["rebalanced"].mean().to_dict()
        max_diff = max(rates.values()) - min(rates.values()) if rates else 0

        return {
            "bias_detected": max_diff > 0.30, #30% disparate impact threshold
            "disparate_impact_delta": max_diff,
            "rebalance_rates_by_profile": rates
        }