import streamlit as st

st.title("🛡️ System Health & Kill-Switch Controls")

# Initialize global safety state
if "kill_switch_active" not in st.session_state:
    st.session_state["kill_switch_active"] = False

# Metric Sliders
vix = st.slider(
    "Current Market Volatility (VIX)",
    min_value=0.0,
    max_value=60.0,
    value=22.50,
    step=0.50,
)
error_rate = st.slider(
    "System Error Rate (%)",
    min_value=0.0,
    max_value=5.0,
    value=0.80,
    step=0.10,
)

# Threshold limits
VIX_THRESHOLD = 35.0
ERROR_THRESHOLD = 2.0

# Dynamic threshold evaluation
auto_kill = vix > VIX_THRESHOLD or error_rate > ERROR_THRESHOLD

col1, col2 = st.columns([3, 1])

with col2:
    if st.button("🚨 MANUAL KILL-SWITCH", type="primary"):
        st.session_state["kill_switch_active"] = True

    if st.button("🔄 Reset System"):
        st.session_state["kill_switch_active"] = False

# Render status banner and synchronize state
if auto_kill or st.session_state["kill_switch_active"]:
    st.session_state["kill_switch_active"] = True
    st.error(
        "🔴 KILL-SWITCH TRIGGERED: Autonomous execution paused. All portfolio rebalancing trades are locked."
    )
else:
    st.success("🟢 System Operational - All safety boundaries within normal limits.")