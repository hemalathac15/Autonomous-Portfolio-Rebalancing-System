import numpy as np
import pytest
from engine.cvxpy_optimizer import PortfolioOptimizer
from engine.drift_calculator import DriftCalculator


def test_drift_calculation():
    target_weights = np.array([0.40, 0.40, 0.20])
    calculator = DriftCalculator(target_weights=target_weights)
    current_weights = np.array([0.50, 0.30, 0.20])

    # Test single-portfolio dictionary method
    drift_results = calculator.compute_drift(current_weights)
    assert "max_drift" in drift_results
    assert drift_results["requires_rebalance"] is True

    # Test vectorized dataframe matrix method
    holdings_matrix = np.array([[50, 30, 20]])
    df_results = calculator.calculate_portfolio_drift(holdings_matrix)
    
    # Cast to bool or check truthiness to handle numpy.bool_
    assert bool(df_results.iloc[0]["requires_rebalance"]) is True
    assert pytest.approx(df_results.iloc[0]["max_drift"], abs=1e-4) == 0.10


def test_portfolio_optimizer():
    optimizer = PortfolioOptimizer(num_assets=3)
    current_w = np.array([0.50, 0.30, 0.20])
    target_w = np.array([0.40, 0.40, 0.20])
    cov_matrix = np.eye(3) * 0.01
    t_costs = np.array([0.001, 0.001, 0.001])

    optimized_w = optimizer.optimize_rebalance(
        current_weights=current_w,
        target_weights=target_w,
        cov_matrix=cov_matrix,
        transaction_costs=t_costs,
        max_turnover=0.20,
    )

    assert pytest.approx(np.sum(optimized_w), abs=1e-4) == 1.0