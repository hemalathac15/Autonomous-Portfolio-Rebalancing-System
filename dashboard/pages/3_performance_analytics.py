import sys
from pathlib import Path

# Add project root directory to sys.path
root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.append(str(root_dir))

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from backtesting.back_test_engine import BacktestEngine
from backtesting.strategy_comparator import StrategyComparator

st.title("📈 Backtesting & Strategy Performance")

engine = BacktestEngine()
backtest_df = engine.run_12m_backtest(np.array([100000]))

st.subheader("12-Month Portfolio Cumulative Return Trajectory")

# Reset index to convert Month column into explicit X-axis variable
df_plot = backtest_df.reset_index()
x_col = df_plot.columns[0]  # First column contains months

# Render using Plotly to lock categorical order
fig = px.line(
    df_plot,
    x=x_col,
    y=["Autonomous_Agent", "Legacy_Quarterly", "Buy_And_Hold"],
    labels={"value": "Cumulative Return", "variable": "Strategy"},
)

# Force category order explicitly
fig.update_xaxes(
    type="category",
    categoryorder="array",
    categoryarray=[f"Month {i}" for i in range(1, 13)],
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Performance & Efficiency Scorecard")
metrics_df = StrategyComparator.calculate_metrics(backtest_df)
st.table(metrics_df)