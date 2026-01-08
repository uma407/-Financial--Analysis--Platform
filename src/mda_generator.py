"""
Automated MD&A Draft Generator (offline-friendly, no external LLM required).
Generates a structured markdown draft using computed KPIs and trends.
"""
from __future__ import annotations

import os
from typing import Dict

import pandas as pd

from src.data_processor import (
    load_financials,
    compute_period_deltas,
    compute_kpis,
    dataframe_to_markdown,
)


class MDAGenerator:
    def __init__(self):
        # OFFLINE_MODE=1 skips any LLM calls (LLM code removed for lightweight runtime)
        self.offline = os.getenv("OFFLINE_MODE", "1") == "1"

    def _format_kpis(self, kpis: Dict[str, float]) -> str:
        if not kpis:
            return "- No KPIs computed (missing columns?)"
        lines = []
        for k, v in kpis.items():
            lines.append(f"- {k}: {v:.4f}")
        return "\n".join(lines)

    def _draft_sections(self, kpis: Dict[str, float]) -> str:
        return (
            "### Trends & Performance\n"
            "- Revenue trend inferred from latest periods; review above table.\n"
            "- Margins reflected in KPIs below.\n\n"
            "### Revenue Drivers\n"
            "- Mix and pricing effects inferred from revenue trajectory.\n\n"
            "### Liquidity & Cash Flows\n"
            "- Operating cash flow vs net income informs quality of earnings.\n\n"
            "### Risks & Uncertainties\n"
            "- Monitor macro sensitivity, concentration, and leverage.\n\n"
            "### KPIs\n"
            f"{self._format_kpis(kpis)}\n"
        )

    def generate_mda(self, csv_path: str) -> str:
        df = load_financials(csv_path)
        df = compute_period_deltas(df)
        kpis = compute_kpis(df)
        context_table = dataframe_to_markdown(df)
        body = self._draft_sections(kpis)
        return f"## Financials (context)\n\n{context_table}\n\n{body}"
