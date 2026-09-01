import numpy as np
import pandas as pd


class DriftCalculator:
    """Vectorized calculation engine to scan 50,000+ portfolios in under 30 seconds."""

    def __init__(self, target_weights: np.ndarray):
        # Target weights across asset classes (e.g., [Eq_IN, Eq_Int, FI_IN, FI_Int, Alts, Cash])
        self.target_weights = np.asarray(target_weights)

    def calculate_portfolio_drift(
        self, current_holdings_matrix: np.ndarray
    ) -> pd.DataFrame:
        """Matrix-based drift calculation.

        current_holdings_matrix shape: (num_portfolios, num_assets) or
        (num_assets,)
        """
        matrix = np.asarray(current_holdings_matrix)

        # Handle 1D single-portfolio input gracefully by expanding dimensions to 2D
        if matrix.ndim == 1:
            matrix = matrix.reshape(1, -1)

        portfolio_values = np.sum(matrix, axis=1, keepdims=True)
        current_weights = matrix / portfolio_values

        # Absolute drift per asset class
        drift_matrix = current_weights - self.target_weights
        max_absolute_drift = np.max(np.abs(drift_matrix), axis=1)

        return pd.DataFrame({
            "current_weights": list(current_weights),
            "drift_matrix": list(drift_matrix),
            "max_drift": max_absolute_drift,
            "requires_rebalance": max_absolute_drift > 0.05,  # 5% threshold
        })

    def compute_drift(self, current_weights: np.ndarray) -> dict:
        """Single portfolio helper method returning a dictionary for quick unit tests."""
        weights = np.asarray(current_weights)

        # Convert to weights if input provided is raw holding values
        if not np.isclose(np.sum(weights), 1.0):
            weights = weights / np.sum(weights)

        drift = weights - self.target_weights
        abs_drift = np.abs(drift)
        max_drift = float(np.max(abs_drift))

        return {
            "current_weights": weights,
            "drift_by_asset": drift,
            "max_drift": max_drift,
            "requires_rebalance": max_drift > 0.05,
        }