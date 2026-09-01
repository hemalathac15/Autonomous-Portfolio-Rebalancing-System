import streamlit as st
import numpy as np
import pandas as pd
from data.synthetic_portfolio_generator import SyntheticPortfolioGenerator

st.title("📊 Portfolio Overview & Heatmap")

@st.cache_data
def load_data():
    gen = SyntheticPortfolioGenerator()
    return gen.generate_portfolios(num_portfolios=1000)

df = load_data()
st.metric(label="Total Monitored Portfolios", value=f"{len(df):,}")

st.subheader("Synthetic Client Population Sample")
st.dataframe(df.head(20), use_container_width=True)

st.subheader("AUM Distribution by Risk Profile")
st.bar_chart(df.groupby("risk_profile")["total_aum"].sum())