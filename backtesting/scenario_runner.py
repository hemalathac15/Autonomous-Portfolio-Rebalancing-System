import numpy as np
import pandas as pd

class ScenarioRunner:
    """Executes market stress test scenarios against rebalancing logic."""

    @staticmethod
    def run_market_crash_scenario(portfolio_weights: np.ndarray, initial_aum: float) -> dict:
        """Scenario 2: COVID-style market crash (-22% Equity IN, -18% Equity INT, +5% Gold)."""
        shock_vector = np.array([-0.22, -0.18, 0.01, -0.02, 0.05, 0.00])
        shocked_values = (portfolio_weights * initial_aum) * (1 + shock_vector)
        new_aum = np.sum(shocked_values)
        post_shock_weights = shocked_values / new_aum
        
        return {
            "pre_crash_aum": initial_aum,
            "post_crash_aum": new_aum,
            "drawdown_pct": (new_aum - initial_aum) / initial_aum,
            "post_shock_weights": post_shock_weights.tolist()
        }