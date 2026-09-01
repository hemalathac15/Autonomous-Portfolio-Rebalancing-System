import numpy as np

class RiskManagerAgent:
    """Agent responsible for checking factor exposure, asset concentration, and volatility limits."""

    def __init__(self, max_concentration_limit: float = 0.50):
        self.max_concentration_limit = max_concentration_limit

    def evaluate_risk(self, proposed_weights: np.ndarray) -> dict:
        max_weight = float(np.max(proposed_weights))
        is_concentrated = max_weight > self.max_concentration_limit

        return {
            "risk_status": "HIGH_RISK" if is_concentrated else "LOW_RISK",
            "max_asset_exposure": max_weight,
            "concentration_breach": is_concentrated
        }