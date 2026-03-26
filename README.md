# 🤖 AI Portfolio Rebalancer (School Project Edition)

### *Technical Deep-Dive: Dynamic Portfolio Optimization Engine*

This project implements a system designed to solve complexities in wealth management through automated data ingestion, mathematical optimization, and structural time-series forecasting.

---

## 🏗️ The Engineering Approach

The system is built as a modular pipeline that transforms raw market data into executable financial strategies:

1.  **Data Ingestion:** Real-time pricing and historical OHLCV data are ingested via the `yfinance` API.
2.  **Statistical Inference:** Covariance matrices and expected returns are computed to model the risk/return profile of the current holdings.
3.  **Optimization Engine:** A quadratic programming solver identifies the "Optimal Weights" on the Efficient Frontier.
4.  **Trade Synthesis:** The delta between current and target weights is translated into fractional trade orders.
5.  **Predictive Modeling:** Structural time-series models (ARIMA & Exponential Smoothing) forecast the expected trajectory of the optimized portfolio, complete with walk-forward backtesting.

---

## 🧪 The Science: Optimization & Math

### 🏎️ Modern Portfolio Theory (MPT) & The Efficient Frontier
At its core, the engine utilizes **Mean-Variance Optimization (MVO)**. By analyzing the historical returns and the variance/covariance of assets, the system identifies the "Efficient Frontier"—the set of portfolios that offer the highest expected return for a defined level of risk.

### ⚖️ Quadratic Utility Functions
The engine optimizes a **Quadratic Utility Function**:
> $U = \mu^T w - \frac{\gamma}{2} w^T \Sigma w$

Where:
- $\mu$ is the expected return vector.
- $w$ is the weight vector.
- $\gamma$ is the risk-aversion coefficient (mapped from the user's SWAN risk settings).
- $\Sigma$ is the covariance matrix.

### 🛡️ L2 Regularization (Shrinkage)
To prevent the optimizer from making extreme, concentrated bets due to historical noise, we implement **L2 Regularization** (or weight shrinkage). This forces the weights to be more distributed, effectively "regularizing" the portfolio toward a more diversified state.

---

## 📈 Time-Series Forecasting & Backtesting

Unlike simple static models, this branch implements advanced time-series analysis to project the optimzed portfolio's future value.

- **ARIMA (AutoRegressive Integrated Moving Average):** Configurable `(p, d, q)` parameters allow users to tune the autoregressive and moving average windows. Includes an auto-tune grid-search algorithm minimizing the Akaike Information Criterion (AIC).
- **Exponential Smoothing (Holt-Winters):** Captures level, trend, and seasonality, allowing users to select between additive and multiplicative components.
- **Walk-Forward Backtesting:** The engine splits the dataset, holding out the last N days (configurable via the UI) as testing data. It calculates quantitative performance metrics (**MAE, RMSE, MAPE**) by comparing the historical predictions directly against the actual ground-truth holdout data.

---

## 🛠️ Technology Stack

- **Optimization Core:** [PyPortfolioOpt](https://github.com/robertmartin8/PyPortfolioOpt) — leveraging the CVXPY convex optimization library for solving quadratic programs.
- **Frontend/UI:** [Streamlit](https://streamlit.io/) — providing a reactive, data-dense interface for real-time visualization.
- **Data Pipeline:** [Pandas](https://pandas.pydata.org/) & [yfinance](https://pypi.org/project/yfinance/) for financial market data.
- **Forecasting Engine:** [Statsmodels](https://www.statsmodels.org/) for ARIMA and Exponential Smoothing.
- **Metrics:** [Scikit-learn](https://scikit-learn.org/) for mean absolute / squared error calculation.

---

## 📉 Risk & Simulations

The system validates its optimized targets through a **Monte Carlo Simulation Engine**, which projects portfolio performance across 252 trading days. It computes probabilities for:
- **Value at Risk (VaR):** The 5th percentile "Worst Case" scenario.
- **Median Growth:** The expected pathway.
- **95th Percentile:** The optimistic market projection.
