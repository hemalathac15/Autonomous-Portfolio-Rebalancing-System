import numpy as np
import streamlit as st
from agents.orchestrator import RebalanceOrchestrator
from explainability.explanation_generator import ExplanationGenerator

st.title("🔍 Explainability Centre")

# Dynamic Portfolio Repository
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

if st.button("Generate Explainability Report"):
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

    # 1. Run Rebalancing Orchestrator to fetch decision payload
    orchestrator = RebalanceOrchestrator(
        target_weights=target_weights, cov_matrix=cov_matrix
    )
    decision_data = orchestrator.process_portfolio(portfolio_id, holdings)

    current_weights = (holdings / np.sum(holdings)).tolist()
    target_weights_list = target_weights.tolist()
    proposed_trades = decision_data.get("trades_required", [0.0] * len(target_weights))

    # 2. Call ExplanationGenerator facade
    generator = ExplanationGenerator()
    explanation = generator.generate_comprehensive_explanation(
        portfolio_id=portfolio_id,
        current_weights=current_weights,
        target_weights=target_weights_list,
        proposed_trades=proposed_trades,
        decision_data=decision_data,
        tax_data={"tax_liability": 0.0},
        compliance_data={"status": "PASSED"},
    )

    # 3. Render dynamic explanations in Streamlit UI
    st.subheader("1. Plain-Language Client Narrative (Grade 8 Level)")
    st.info(explanation["narratives"]["client"])

    st.subheader("2. Advisor Detailed Report")
    st.markdown(explanation["narratives"]["advisor"])

    st.subheader("3. Counterfactual Explanation ('What-If' Analysis)")
    st.warning(str(explanation["counterfactual_analysis"]))

    st.subheader("4. SHAP Feature Attributions & Audit Log")
    st.json({
        "shap_attributions": explanation["shap_attributions"],
        "compliance": explanation["narratives"]["compliance"],
    })