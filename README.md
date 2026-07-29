# Portfolio Risk & Return Dashboard

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**🔗 Live app: [https://your-actual-url.streamlit.app](https://your-actual-url.streamlit.app)**

An interactive Streamlit app for analyzing the risk and return characteristics of a stock 
portfolio. Pick stocks from a 50-ticker stock list covering 9 sectors, set your own portfolio 
weights, and get back key risk metrics computed from historical daily price data pulled via 
`yfinance`.

## Features

- **Stock collection**: 50 tickers across Tech, Consumer Goods, Comms/Media, Finance, Healthcare, 
  Industrials, Energy, Consumer Staples, Utilities, and broad market ETFs (SPY, QQQ)
- **Custom weighting**: assign a % weight to each selected stock, with a live check that weights 
  sum to 100%
- **Adjustable lookback period**: 30 to 1825 days
- **Adjustable risk-free rate**: used in Sharpe ratio calculations
- **Per-stock statistics**: annualized return, annualized volatility, and Sharpe ratio
- **Correlation heatmap**: visualizes how selected stocks move together (or don't), useful for 
  spotting real diversification vs. redundant exposure
- **Max drawdown**: worst historical peak-to-trough decline per stock, plus a chart of drawdown 
  over time
- **Portfolio-level statistics**: annualized return, volatility, and Sharpe ratio for the 
  portfolio as a whole, calculated using the full covariance matrix (not just a weighted average 
  of individual stock volatilities)

## Tech Stack

Python, Streamlit, yfinance, pandas, NumPy, seaborn, matplotlib

## Run locally in cmd

```
pip install -r requirements.txt
streamlit run app.py
```

## How it works

1. Select stocks from the dropdown
2. Set a lookback period and risk-free rate
3. Assign a weight (%) to each stock — must sum to 100%
4. Click "Analyze" to pull historical price data and generate:
   - a per-stock stats table (return, volatility, Sharpe)
   - a correlation heatmap
   - a max drawdown chart
   - portfolio-level return, volatility, and Sharpe ratio

## Limitations

- Risk-free rate is manually set, not taken from live Treasury yield data
- No transaction costs, taxes, or rebalancing assumptions
- Based purely on historical price data — not a predictive or forward-looking model
- Portfolio weights are static over the lookback period (no rebalancing simulated)
