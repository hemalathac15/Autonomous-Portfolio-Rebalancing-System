import numpy as np
import streamlit as st
from agents.orchestrator import RebalanceOrchestrator

st.title("⚡ Rebalancing Execution Engine")

# Central Portfolio Mock DB
PORTFOLIO_DB = {
    "PORT_000042": {
        "holdings_pct": np.array([0.55, 0.10, 0.20, 0.05, 0.05, 0.05]),
        "target_weights": np.array([0.40, 0.15, 0.25, 0.10, 0.05, 0.05]),
    },
    "PORT_000001": {
        "holdings_pct": np.array([0.30, 0.30, 0.15, 0.15, 0.05, 0.05]),
        "target_weights": np.array([0.35, 0.25, 0.20, 0.10, 0.05, 0.05]),
    },
    "PORT_000002": {
        "holdings_pct": np.array([0.60, 0.05, 0.15, 0.10, 0.05, 0.05]),
        "target_weights": np.array([0.45, 0.20, 0.20, 0.05, 0.05, 0.05]),
    },
}

portfolio_id = st.text_input("Enter Portfolio ID", "PORT_000042")
aum = st.number_input("Portfolio AUM (₹)", value=1000000)

if st.button("Run Rebalancing Agent Cycle"):
    # Safety Check: Verify if Kill-Switch is active before running execution cycle
    if st.session_state.get("kill_switch_active", False):
        st.error(
            "🔴 Execution Blocked: System Kill-Switch is currently active! "
            "Please reset the control panel in System Health before attempting a rebalance."
        )
    else:
        if portfolio_id in PORTFOLIO_DB:
            p_data = PORTFOLIO_DB[portfolio_id]
            target_weights = p_data["target_weights"]
            holdings = p_data["holdings_pct"] * aum
        else:
            seed = abs(hash(portfolio_id)) % (2**32)
            np.random.seed(seed)
            raw_holdings = np.random.dirichlet(np.ones(6))
            holdings = raw_holdings * aum
            target_weights = np.array([0.40, 0.15, 0.25, 0.10, 0.05, 0.05])

        cov_matrix = np.eye(len(target_weights)) * 0.02

        # Initialize orchestrator with dynamic target weights & covariance matrix
        orchestrator = RebalanceOrchestrator(
            target_weights=target_weights, cov_matrix=cov_matrix
        )

        result = orchestrator.process_portfolio(portfolio_id, holdings)

        st.success(f"Agent cycle executed successfully for {portfolio_id}")
        st.json(result)