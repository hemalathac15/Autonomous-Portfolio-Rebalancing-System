import numpy as np
from engine.drift_calculator import DriftCalculator


class PortfolioAnalystAgent:
    """Agent responsible for scanning portfolio drift and evaluating threshold/event triggers."""

    def __init__(self, default_target_weights: np.ndarray = None):
        self.default_target_weights = default_target_weights

    def analyze(
        self,
        portfolio_id: str,
        holdings: np.ndarray,
        target_weights: np.ndarray = None,
    ) -> dict:
        # Use passed target_weights, fallback to default, or fail gracefully
        target = (
            target_weights
            if target_weights is not None
            else self.default_target_weights
        )

        if target is None:
            raise ValueError(
                f"No target weights provided for portfolio {portfolio_id}."
            )

        drift_calc = DriftCalculator(target)
        drift_df = drift_calc.calculate_portfolio_drift(
            holdings.reshape(1, -1)
        )

        max_drift = drift_df["max_drift"].iloc[0]
        requires_rebalance = drift_df["requires_rebalance"].iloc[0]

        return {
            "portfolio_id": portfolio_id,
            "max_drift_pct": float(max_drift * 100),
            "trigger_fired": (
                "THRESHOLD_DRIFT" if requires_rebalance else "NONE"
            ),
            "requires_rebalance": bool(requires_rebalance),
        }