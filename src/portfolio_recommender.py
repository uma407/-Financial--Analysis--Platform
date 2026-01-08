"""
Portfolio recommender using a lightweight mean-variance heuristic (no external solvers).
"""
from __future__ import annotations

from typing import Dict, Any
import os

import pandas as pd
import numpy as np

from config import RISK_FREE_RATE, MAX_PORTFOLIO_WEIGHT


class PortfolioRecommender:
    def __init__(self):
        # OFFLINE_MODE=1 -> skip any LLM calls (none are used now)
        self.offline = os.getenv("OFFLINE_MODE", "1") == "1"

    def _load_prices(self, csv_path: str) -> pd.DataFrame:
        df = pd.read_csv(csv_path, parse_dates=True, index_col=0)
        return df

    def _risk_aversion(self, risk_tolerance: str) -> float:
        mapping = {
            "conservative": 8.0,
            "moderate": 4.0,
            "aggressive": 1.5,
        }
        return mapping.get(risk_tolerance.lower(), 4.0)

    def _project_weights(self, w: np.ndarray) -> np.ndarray:
        """Project weights to simplex with per-asset cap."""
        w = np.clip(w, 0, MAX_PORTFOLIO_WEIGHT)
        total = w.sum()
        if total == 0:
            w = np.ones_like(w) / len(w)
        else:
            w = w / total
        # If still violates cap after normalization, iteratively cap and renormalize
        over = w > MAX_PORTFOLIO_WEIGHT
        while over.any():
            excess = (w[over] - MAX_PORTFOLIO_WEIGHT).sum()
            w[over] = MAX_PORTFOLIO_WEIGHT
            remaining = (~over).sum()
            if remaining == 0:
                break
            w[~over] += excess / remaining
            over = w > MAX_PORTFOLIO_WEIGHT
        return w

    def recommend_portfolio(
        self,
        csv_path: str,
        risk_tolerance: str = "moderate",
        investment_horizon: int = 10,
        initial_capital: float = 100_000,
    ) -> Dict[str, Any]:
        prices = self._load_prices(csv_path)
        log_returns = np.log(prices / prices.shift(1)).dropna()
        mu = log_returns.mean() * 252  # annualized
        cov = log_returns.cov() * 252

        # Simple mean-variance closed form: w ~ inv(cov + lambda*I) * mu
        lam = self._risk_aversion(risk_tolerance)
        cov_reg = cov + np.eye(cov.shape[0]) * lam
        inv_cov = np.linalg.pinv(cov_reg)
        raw_w = inv_cov @ mu.values
        weights = self._project_weights(raw_w)

        cleaned_weights = {asset: float(w) for asset, w in zip(mu.index, weights)}
        exp_return = float(np.dot(weights, mu.values))
        volatility = float(np.sqrt(weights @ cov.values @ weights))
        sharpe = (exp_return - RISK_FREE_RATE) / (volatility + 1e-9)

        allocation = {
            "weights": cleaned_weights,
            "expected_return": exp_return,
            "volatility": volatility,
            "sharpe_ratio": sharpe,
            "initial_capital": initial_capital,
            "allocation_amounts": {
                asset: weight * initial_capital for asset, weight in cleaned_weights.items()
            },
        }

        explanation = (
            "Offline mode: allocation explanation generated without LLM. "
            "Weights emphasize diversification with risk-adjusted balance."
        )

        allocation["llm_explanation"] = explanation
        return allocation
