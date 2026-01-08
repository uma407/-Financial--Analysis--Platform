# Financial Analysis Platform

A comprehensive platform for automated financial analysis featuring:
1. **Automated MD&A Draft Generator** - Generate Management Discussion & Analysis narratives from financial statements using RAG
2. **Portfolio Recommender Agent** - AI-powered portfolio allocation based on risk profile

## Features

### F1: Automated MD&A Draft Generator
- Loads financial statements and computes YoY/QoQ deltas
- Calculates key performance indicators (KPIs)
- Uses RAG (Retrieval-Augmented Generation) to generate sectioned markdown drafts
- Produces narratives covering trends, revenue drivers, and risks
- Includes citations to source chunks

### F2: Portfolio Recommender Agent
- Risk profile assessment
- Modern Portfolio Theory (MPT) optimization
- Black-Litterman variant support
- Plain English explanations via LLM
- JSON export of portfolio weights

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd "Automated MD&A Draft from Financials (RAG + Summarization)"
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory:
```
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here  # Optional
```

## Usage

### Running the Streamlit App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Using the Python Modules

#### MD&A Generator
```python
from src.mda_generator import MDAGenerator

generator = MDAGenerator()
draft = generator.generate_mda("path/to/financial_data.csv")
print(draft)
```

#### Portfolio Recommender
```python
from src.portfolio_recommender import PortfolioRecommender

recommender = PortfolioRecommender()
allocation = recommender.recommend_portfolio(
    risk_tolerance="moderate",
    investment_horizon=10,
    initial_capital=100000
)
print(allocation)
```

## Data Sources

The project is designed to work with:
- **Financial Statement Extracts (SEC)**: https://www.kaggle.com/datasets/securities-exchange-commission/financialstatement-extracts
- **Stock Portfolio Data**: https://www.kaggle.com/datasets/nikitamanaenkov/stock-portfolio-data-with-pricesand-indices

Place your data files in the `data/` directory.

## Project Structure

```
.
├── app.py                 # Streamlit main application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── src/
│   ├── __init__.py
│   ├── mda_generator.py  # MD&A generation module
│   ├── portfolio_recommender.py  # Portfolio recommendation module
│   ├── data_processor.py # Data processing utilities
│   └── vector_store.py   # Vector store management
├── data/                 # Data directory (create this)
└── utils/
    └── __init__.py
```

## Technologies

- **Python 3.9+**
- **LangChain** - LLM orchestration
- **OpenAI** - Embeddings and chat models
- **ChromaDB/FAISS** - Vector stores
- **Streamlit** - Frontend framework
- **PyPortfolioOpt/cvxpy** - Portfolio optimization
- **Pandas** - Data manipulation
- **Plotly** - Data visualization

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
