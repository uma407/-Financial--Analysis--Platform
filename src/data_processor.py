"""
Data processing utilities for financial statements and text chunking.
"""
from __future__ import annotations

import os
from typing import List, Dict, Tuple

import pandas as pd

from config import DATA_DIR


def ensure_data_dir(path: str = DATA_DIR) -> None:
    """Create the data directory if it does not exist."""
    os.makedirs(path, exist_ok=True)


def load_financials(csv_path: str) -> pd.DataFrame:
    """Load financial statements from CSV."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Financial data not found at {csv_path}")
    df = pd.read_csv(csv_path)
    
    # Validate required columns
    required_cols = ["period"]
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        available_cols = ", ".join(df.columns.tolist())
        raise ValueError(
            f"Missing required columns: {', '.join(missing_cols)}\n"
            f"Available columns in CSV: {available_cols}\n"
            f"Expected columns: period, revenue, net_income, total_assets, total_liabilities, operating_cash_flow"
        )
    return df


def compute_period_deltas(
    df: pd.DataFrame,
    date_col: str = "period",
    value_cols: List[str] | None = None,
) -> pd.DataFrame:
    """
    Compute YoY and QoQ deltas for numeric columns.
    Expects period column parseable as datetime.
    """
    df = df.copy()
    if date_col not in df.columns:
        raise KeyError(
            f"Column '{date_col}' not found in dataframe.\n"
            f"Available columns: {', '.join(df.columns.tolist())}"
        )
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col)

    if value_cols is None:
        value_cols = [c for c in df.columns if c != date_col and pd.api.types.is_numeric_dtype(df[c])]

    for col in value_cols:
        df[f"{col}_qoq"] = df[col].pct_change(periods=1)
        df[f"{col}_yoy"] = df[col].pct_change(periods=4)
    return df


def compute_kpis(df: pd.DataFrame) -> Dict[str, float]:
    """
    Compute simple KPIs from financial statements.
    Expected columns: revenue, net_income, total_assets, total_liabilities, operating_cash_flow.
    """
    if "period" not in df.columns:
        # If no period column, just use the last row
        latest = df.iloc[-1]
    else:
        latest = df.sort_values("period").iloc[-1]
    kpis: Dict[str, float] = {}

    revenue = latest.get("revenue")
    net_income = latest.get("net_income")
    total_assets = latest.get("total_assets")
    total_liabilities = latest.get("total_liabilities")
    op_cf = latest.get("operating_cash_flow")

    if revenue and total_assets:
        kpis["asset_turnover"] = revenue / total_assets
    if net_income and revenue:
        kpis["net_margin"] = net_income / revenue
    if net_income and total_assets:
        kpis["roa"] = net_income / total_assets
    if net_income and (total_assets and total_liabilities is not None):
        equity = total_assets - total_liabilities
        if equity:
            kpis["roe"] = net_income / equity
    if op_cf and net_income:
        kpis["quality_of_earnings"] = op_cf / net_income
    return kpis


def dataframe_to_markdown(df: pd.DataFrame, max_rows: int = 20) -> str:
    """Convert a dataframe to markdown table for context."""
    df = df.head(max_rows)
    return df.to_markdown(index=False)


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """Simple text chunker."""
    tokens = text.split()
    chunks = []
    start = 0
    while start < len(tokens):
        end = min(len(tokens), start + chunk_size)
        chunk = " ".join(tokens[start:end])
        chunks.append(chunk)
        start = max(start + chunk_size - overlap, end)
    return chunks


def make_financial_text(df: pd.DataFrame) -> str:
    """Render the financial dataframe into a narrative-like text for embedding."""
    return df.to_csv(index=False)


def split_filings(filings: List[Tuple[str, str]], chunk_size: int, overlap: int) -> List[Dict[str, str]]:
    """
    Chunk filings into documents for vector storage.
    filings: list of (filing_id, text)
    """
    documents: List[Dict[str, str]] = []
    for filing_id, text in filings:
        for idx, chunk in enumerate(chunk_text(text, chunk_size=chunk_size, overlap=overlap)):
            documents.append(
                {
                    "id": f"{filing_id}_chunk_{idx}",
                    "source_id": filing_id,
                    "text": chunk,
                }
            )
    return documents
