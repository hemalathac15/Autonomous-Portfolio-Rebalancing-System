import numpy as np
from engine.cvxpy_optimizer import PortfolioOptimizer
from engine.drift_calculator import DriftCalculator


class RebalanceOrchestrator:
    """Agent orchestrating the end-to-end evaluation and rebalancing pipeline."""

    def __init__(
        self, target_weights: np.ndarray, cov_matrix: np.ndarray = None
    ):
        self.target_weights = target_weights
        self.cov_matrix = (
            cov_matrix
            if cov_matrix is not None
            else np.eye(len(target_weights)) * 0.02
        )
        self.drift_calc = DriftCalculator(target_weights)
        self.optimizer = PortfolioOptimizer(num_assets=len(target_weights))

    def process_portfolio(self, portfolio_id: str, holdings: np.ndarray) -> dict:
        drift_df = self.drift_calc.calculate_portfolio_drift(
            holdings.reshape(1, -1)
        )
        requires_rebalance = drift_df["requires_rebalance"].iloc[0]

        if not requires_rebalance:
            return {
                "portfolio_id": portfolio_id,
                "action": "HOLD",
                "reason": "Drift within acceptable bands (<5%).",
            }

        current_weights = holdings / np.sum(holdings)
        transaction_costs = np.full(len(current_weights), 0.001)

        optimized_weights = self.optimizer.optimize_rebalance(
            current_weights=current_weights,
            target_weights=self.target_weights,
            cov_matrix=self.cov_matrix,
            transaction_costs=transaction_costs,
        )

        return {
            "portfolio_id": portfolio_id,
            "action": "REBALANCE",
            "current_weights": current_weights.tolist(),
            "target_weights": self.target_weights.tolist(),
            "optimized_weights": optimized_weights.tolist(),
            "trades_required": (optimized_weights - current_weights).tolist(),
        }