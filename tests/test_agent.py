import numpy as np
from agents.orchestrator import RebalanceOrchestrator


def test_orchestrator_initialization():
    # Define sample target weights and covariance matrix for 4 assets
    target_weights = np.array([0.40, 0.30, 0.20, 0.10])
    cov_matrix = np.eye(4) * 0.04  # 4x4 identity matrix with 4% variance

    orchestrator = RebalanceOrchestrator(
        target_weights=target_weights, cov_matrix=cov_matrix
    )
    assert orchestrator is not None