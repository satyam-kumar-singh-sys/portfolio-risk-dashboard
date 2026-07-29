import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns #used for the correlation heatmap
import matplotlib.pyplot as plt #used for the correlation heatmap

st.title("Portfolio Risk & Return Dashboard")

# Using tickers from a variety of sectors as input
tickers = st.multiselect(
    "Pick your stocks",
    [
    # Tech:
    "AAPL", "MSFT", "NVDA", "GOOGL", "META", "AVGO", "ORCL", "CRM", "ADBE", "AMD",
    # Consumer Goods:
    "AMZN", "TSLA", "HD", "NKE", "MCD", "SBUX", "LOW", "TJX",
    # Comms/Media:
    "NFLX", "DIS", "CMCSA",
    # Finance:
    "JPM", "BAC", "WFC", "GS", "MS", "V", "MA", "AXP",
    # Healthcare
    "LLY", "UNH", "JNJ", "PFE", "ABBV", "MRK", "TMO",
    # Industrials
    "BA", "CAT", "GE", "HON", "UPS",
    # Energy
    "XOM", "CVX", "COP",
    # Consumer Staples:
    "PG", "KO", "PEP", "WMT", "COST",
    # Utilities: (low correlation to tech)
    "NEE", "DUK",
    # Broad market ETFs: 
    "SPY", "QQQ"
]
)
 

days = st.slider("Lookback period (days)", 30, 1825, 365)
risk_free_rate = st.number_input("Risk-free rate (annual, e.g. 0.04 = 4%)", value=0.04, step=0.01)

weights = {}
if tickers:
    st.subheader("Set portfolio weights (%)")

    for i, t in enumerate(tickers):
        default = round(100 / len(tickers), 2)
        w = st.number_input(f"{t} weight (%)", min_value=0.0, max_value=100.0, value=default, key=f"w_{t}")
        weights[t] = w

    total_weight = sum(weights.values())
    if abs(total_weight - 100) > 0.01:
        st.warning(f"Weights currently sum to {total_weight:.2f}%. They should sum to 100%.")

if st.button("Analyze") and tickers:
    # Generating the data
    df = yf.download(tickers, period=f"{days}d", auto_adjust=False)["Close"]
    if isinstance(df, pd.Series):  # only happens if 1 ticker selected
        # yfinance returns a Series instead of dataframe when only 1 ticker is picked
        # to counter that, I convert it back into a dataframe object
        df = df.to_frame(name=tickers[0])

    daily_returns = df.pct_change().dropna()

    # Per-Stock Stats
    st.subheader("Per-Stock Statistics")
    annual_vol = daily_returns.std() * np.sqrt(252)
    annual_return = daily_returns.mean() * 252
    sharpe = (annual_return - risk_free_rate) / annual_vol

    stats_df = pd.DataFrame({
        "Annualized Return": annual_return,
        "Annualized Volatility": annual_vol,
        "Sharpe Ratio": sharpe
    })
    st.dataframe(stats_df.style.format("{:.2%}", subset=["Annualized Return", "Annualized Volatility"])
                              .format("{:.2f}", subset=["Sharpe Ratio"]))

    # Generating a Correlation heatmap
    st.subheader("Correlation Matrix")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(daily_returns.corr(), annot=True, cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
    st.pyplot(fig)

    # Max Drawdown (worst peak to trough drop -> how much would you lose if you bought on peak
    # and sold at trough)
    st.subheader("Max Drawdown")
    cum_returns = (1 + daily_returns).cumprod()
    running_max = cum_returns.cummax()
    drawdown = (cum_returns - running_max) / running_max
    st.line_chart(drawdown)
    st.write(drawdown.min().rename("Max Drawdown").apply(lambda x: f"{x:.2%}"))

    # Portfolio-level stats (using weights)
    if abs(total_weight - 100) < 0.01:  # only compute if weights are valid
        st.subheader("Portfolio-Level Statistics")
        w = np.array([weights[t] / 100 for t in tickers])  # convert % to decimals
        cov_matrix = daily_returns.cov() * 252  # annualized covariance

        port_return = np.dot(w, annual_return)
        port_variance = w @ cov_matrix @ w.T
        port_vol = np.sqrt(port_variance)
        port_sharpe = (port_return - risk_free_rate) / port_vol

        st.write(f"**Portfolio Annualized Return:** {port_return:.2%}")
        st.write(f"**Portfolio Annualized Volatility:** {port_vol:.2%}")
        st.write(f"**Portfolio Sharpe Ratio:** {port_sharpe:.2f}")
    else:
        st.info("Ensure weights sum up to 100% to see portfolio-level stats.")