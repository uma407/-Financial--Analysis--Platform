# Output Examples

This document shows example outputs from running the Financial Analysis Platform.

## Repository URL
**https://github.com/uma407/-Financial--Analysis--Platform.git**

## F1: MD&A Draft Generator Output

### Sample Input
Financial statements CSV with columns: `period, revenue, net_income, total_assets, total_liabilities, operating_cash_flow`

### Sample Output

```
## Financials (context)

| period              |   revenue |   net_income |   total_assets |   total_liabilities |   operating_cash_flow |   revenue_qoq |   revenue_yoy |   net_income_qoq |   net_income_yoy |   total_assets_qoq |   total_assets_yoy |   total_liabilities_qoq |   total_liabilities_yoy |   operating_cash_flow_qoq |   operating_cash_flow_yoy |
|:--------------------|----------:|-------------:|---------------:|--------------------:|----------------------:|--------------:|--------------:|-----------------:|-----------------:|-------------------:|-------------------:|------------------------:|------------------------:|--------------------------:|--------------------------:|
| 2020-01-01 00:00:00 |   1000000 |       100000 |        5000000 |             3000000 |                120000 |   nan         |    nan        |      nan         |       nan        |        nan         |         nan        |             nan         |              nan        |               nan         |                nan        |
| 2020-04-01 00:00:00 |   1100000 |       110000 |        5200000 |             3100000 |                130000 |     0.1       |    nan        |        0.1       |       nan        |          0.04      |         nan        |               0.0333333 |              nan        |                 0.0833333 |                nan        |
...

### Trends & Performance
- Revenue trend inferred from latest periods; review above table.
- Margins reflected in KPIs below.

### Revenue Drivers
- Mix and pricing effects inferred from revenue trajectory.

### Liquidity & Cash Flows
- Operating cash flow vs net income informs quality of earnings.

### Risks & Uncertainties
- Monitor macro sensitivity, concentration, and leverage.

### KPIs
- asset_turnover: 0.3125
- net_margin: 0.1260
- roa: 0.0394
- roe: 0.0900
- quality_of_earnings: 0.8571
```

**Key Features:**
- Computes YoY and QoQ deltas automatically
- Calculates financial KPIs (ROA, ROE, margins, etc.)
- Generates structured markdown sections
- Includes source data table with computed metrics

---

## F2: Portfolio Recommender Output

### Sample Input
Portfolio data CSV with date index and asset price columns (e.g., AAPL, MSFT, GOOGL, TLT, GLD)

### Sample Output

```json
{
  "weights": {
    "AAPL": 0.25,
    "MSFT": 0.25,
    "GOOGL": 0.25,
    "TLT": 0.0,
    "GLD": 0.25
  },
  "expected_return": 4.120292918907841,
  "volatility": 0.24527690911400304,
  "sharpe_ratio": 16.716995158663952,
  "initial_capital": 100000,
  "allocation_amounts": {
    "AAPL": 25000.0,
    "MSFT": 25000.0,
    "GOOGL": 25000.0,
    "TLT": 0.0,
    "GLD": 25000.0
  },
  "llm_explanation": "Offline mode: allocation explanation generated without LLM. Weights emphasize diversification with risk-adjusted balance."
}
```

**Key Features:**
- Risk-adjusted portfolio optimization
- Supports conservative, moderate, and aggressive risk profiles
- Calculates expected return, volatility, and Sharpe ratio
- Provides allocation amounts based on initial capital
- Exports JSON for further analysis

---

## Running the Application

### Command Line Test
```bash
# Test MD&A Generator
python -c "from src.mda_generator import MDAGenerator; gen = MDAGenerator(); print(gen.generate_mda('data/financial_statements.csv'))"

# Test Portfolio Recommender
python -c "from src.portfolio_recommender import PortfolioRecommender; import json; rec = PortfolioRecommender(); print(json.dumps(rec.recommend_portfolio('data/portfolio_data.csv', 'moderate', 10, 100000), indent=2))"
```

### Streamlit Web App
```bash
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

---

## Project Status

✅ **Completed:**
- MD&A Draft Generator with KPI computation
- Portfolio Recommender with risk profiling
- Streamlit frontend
- Sample data files
- Code pushed to GitHub

🔗 **Repository:** https://github.com/uma407/-Financial--Analysis--Platform.git
