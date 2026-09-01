import cvxpy as cp
import numpy as np

class PortfolioOptimizer:
    """Quadratic Programming optimization engine using CVXPY."""

    def __init__(self, num_assets: int = 6):
        self.num_assets = num_assets

    def optimize_rebalance(
        self, 
        current_weights: np.ndarray,
        target_weights: np.ndarray,
        cov_matrix: np.ndarray,
        transaction_costs: np.ndarray,
        max_turnover: float = 0.20
    ) -> np.ndarray:
        """
        Minimizes tracking error subject to turnover, long-only, and cost constraints.
        """
        w = cp.Variable(self.num_assets)

        #Objective Minimize tracking error variance + transaction cost penalty
        tracking_error = cp.quad_form(w-target_weights, cov_matrix)
        turnover_cost = cp.sum(cp.multiply(transaction_costs, cp.abs(w-current_weights)))
        objective = cp.Minimize(tracking_error + turnover_cost)

        #Constraints
        constraints = [
            cp.sum(w) == 1.0,       #Fully invested
            w >= 0.0,               #Long-only constraint
            cp.sum(cp.abs(w-current_weights)) <= max_turnover #Turnover budget
        ]

        problem = cp.Problem(objective, constraints)
        problem.solve(solver=cp.OSQP)

        return w.value if problem.status == cp.OPTIMAL else current_weights