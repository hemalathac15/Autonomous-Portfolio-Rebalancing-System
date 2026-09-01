import streamlit as st

st.set_page_config(
    page_title = "Autonomous Portfolio Rebalancing System",
    page_icon = "📈",
    layout = "wide"
)

st.title("📈 Autonomous Portfolio Rebalancing System")
st.markdown("""
Welcome to the Autonomous Portfolio Rebalancing System.
### Multi-Page Navigation
* **Portfolio Overview**: View synthetic client population and asset drift heatmaps.
* **Rebalancing Activity**: System decision logs, multi-agent signals, and CVXPY trade execution.
* **Performance Analytics**: 12-month backtesting  performance and strategy comparison.
* **Explainability Centre**: Client-facing narratives and Tree SHAP/LIME feature attributions.
* **System Health**: Human-in-the-Loop kill-switch controls, error rates, and compliance audits.
""")

st.sidebar.success("Select a dashboard view above.")