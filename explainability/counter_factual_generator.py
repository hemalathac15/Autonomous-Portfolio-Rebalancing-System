import numpy as np


class CounterfactualGenerator:
    """Generates counterfactual explanations ('What-if' boundaries)."""

    @staticmethod
    def get_counterfactual(current_drift: float, threshold: float = 0.05) -> str:
        """Computes text narrative based on raw drift values (e.g., 0.078 for 7.8%)."""
        if current_drift < threshold:
            delta = (threshold - current_drift) * 100
            return f"Rebalancing would NOT have been triggered unless market drift increased by an additional {delta:.2f}%."
        else:
            delta = (current_drift - threshold) * 100
            return f"Rebalancing was triggered because drift exceeded threshold by {delta:.2f}%. If drift had been {delta:.2f}% lower, no trades would be generated."

    def generate_what_if(
        self,
        current_weights: list = None,
        target_weights: list = None,
        market_volatility_pct: float = 0.15,
        current_drift: float = None,
        threshold: float = 0.05,
        **kwargs,
    ) -> dict:
        """Facade adapter method called by ExplanationGenerator.
        
        Dynamically computes current drift from weight vectors if not directly passed.
        """
        if current_drift is None and current_weights is not None and target_weights is not None:
            c_w = np.array(current_weights)
            t_w = np.array(target_weights)
            current_drift = float(np.max(np.abs(c_w - t_w)))
        elif current_drift is None:
            current_drift = 0.0

        narrative = self.get_counterfactual(current_drift=current_drift, threshold=threshold)
        delta_pct = abs(current_drift - threshold) * 100

        return {
            "current_drift_pct": round(current_drift * 100, 2),
            "threshold_pct": round(threshold * 100, 2),
            "delta_pct": round(delta_pct, 2),
            "market_volatility_pct": market_volatility_pct,
            "narrative": narrative,
        }