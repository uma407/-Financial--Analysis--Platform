"""
Streamlit frontend for:
- Automated MD&A Draft Generator (RAG + summarization)
- Portfolio Recommender Agent
"""
from __future__ import annotations

import json
import os
import time

import pandas as pd
import streamlit as st

from config import SAMPLE_FINANCIAL_DATA, SAMPLE_PORTFOLIO_DATA, DATA_DIR
from src.mda_generator import MDAGenerator
from src.portfolio_recommender import PortfolioRecommender
from src.data_processor import ensure_data_dir


st.set_page_config(
    page_title="Financial Analysis Platform",
    page_icon="📊",
    layout="wide",
)


def show_header():
    st.title("📊 Financial Analysis Platform")
    st.write(
        "Generate MD&A drafts and portfolio recommendations with LLMs, RAG, and quantitative models."
    )


def load_uploaded_csv(uploaded_file, dest_path):
    ensure_data_dir(DATA_DIR)
    if uploaded_file is not None:
        with open(dest_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return dest_path
    return None


def page_mda():
    st.subheader("Automated MD&A Draft Generator")
    uploaded = st.file_uploader("Upload financial statements CSV", type=["csv"])
    sample_path = SAMPLE_FINANCIAL_DATA

    col1, col2 = st.columns(2)
    with col1:
        st.caption("Expected columns: period, revenue, net_income, total_assets, total_liabilities, operating_cash_flow")
    with col2:
        st.caption(f"Sample path (if present): {sample_path}")

    if st.button("Generate MD&A Draft"):
        with st.spinner("Generating draft..."):
            csv_path = load_uploaded_csv(uploaded, sample_path) or sample_path
            if not os.path.exists(csv_path):
                st.error("CSV not found. Upload a file or place sample at data/financial_statements.csv")
                return
            generator = MDAGenerator()
            draft = generator.generate_mda(csv_path)
            st.markdown(draft)


def page_portfolio():
    st.subheader("Portfolio Recommender Agent")
    uploaded = st.file_uploader("Upload historical price data (wide CSV with date index)", type=["csv"])
    sample_path = SAMPLE_PORTFOLIO_DATA

    col1, col2, col3 = st.columns(3)
    risk = col1.selectbox("Risk tolerance", ["conservative", "moderate", "aggressive"], index=1)
    horizon = col2.number_input("Investment horizon (years)", min_value=1, max_value=50, value=10)
    capital = col3.number_input("Initial capital", min_value=1000.0, value=100000.0, step=1000.0)

    if st.button("Recommend Portfolio"):
        with st.spinner("Optimizing..."):
            csv_path = load_uploaded_csv(uploaded, sample_path) or sample_path
            if not os.path.exists(csv_path):
                st.error("CSV not found. Upload a file or place sample at data/portfolio_data.csv")
                return
            recommender = PortfolioRecommender()
            result = recommender.recommend_portfolio(
                csv_path=csv_path,
                risk_tolerance=risk,
                investment_horizon=horizon,
                initial_capital=capital,
            )

            st.markdown("### Allocation Weights")
            st.json(result["weights"])

            st.markdown("### Allocation Amounts")
            st.json(result["allocation_amounts"])

            st.markdown("### Performance Metrics")
            st.write(
                {
                    "expected_return": result["expected_return"],
                    "volatility": result["volatility"],
                    "sharpe_ratio": result["sharpe_ratio"],
                }
            )

            st.markdown("### Explanation")
            st.write(result["llm_explanation"])

            st.download_button(
                label="Download allocation JSON",
                data=json.dumps(result, indent=2),
                file_name="portfolio_allocation.json",
                mime="application/json",
            )


def main():
    show_header()
    tab1, tab2 = st.tabs(["MD&A Generator", "Portfolio Recommender"])
    with tab1:
        page_mda()
    with tab2:
        page_portfolio()


if __name__ == "__main__":
    main()
