# 🤖 AI Portfolio Rebalancer

### *Technical Deep-Dive: Dynamic Portfolio Optimization Engine*

This project implements an AI-native system designed to solve the complexities of modern wealth management through automated data ingestion, mathematical optimization, and precision trade execution.

---

## 🏗️ The Engineering Approach

The system is built as a modular pipeline that transforms raw market data into executable financial strategies:

1.  **Data Ingestion:** Real-time pricing and historical OHLCV data are ingested via the `yfinance` API.
2.  **Statistical Inference:** Covariance matrices and expected returns are computed to model the risk/return profile of the current holdings.
3.  **Optimization Engine:** A quadratic programming solver identifies the "Optimal Weights" on the Efficient Frontier.
4.  **Trade Synthesis:** The delta between current and target weights is translated into fractional trade orders.
5.  **AI translation:** Optionally, Google Gemini LLM is used to synthesize mathematical trade rationales into human-readable narratives.

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
To prevent the optimizer from making extreme, concentrated bets due to historical noise, we implement **L2 Regularization** (or weight shrinkage). This forces the weights to be more distributed, effectively "regularizing" the portfolio toward a more diversified state, even when the pure math suggests a concentrated allocation.

---

## 🇨🇦 Mathematical Implementations

### Precision Fractional Rebalancing
Unlike traditional rebalancers that round to the nearest whole share, this engine calculates **fractional trade sizing** to four decimal places. This architectural choice minimizes "cash drag"—the value lost when uninvested cash remains in an account due to rounding constraints.

### Canadian Tax Logic Engine
The system includes a specialized tax module that implements the **50% Capital Gains Inclusion Rule**.
- **Taxable Accounts:** Estimates the tax hit by computing $Gain \times 0.5 \times MarginalRate$.
- **Sheltered Accounts:** Automatically flags TFSA, RRSP, and FHSA accounts to skip gain-calculation logic, treating them as tax-free growth vehicles.

---

## 🛠️ Technology Stack

- **Optimization Core:** [PyPortfolioOpt](https://github.com/robertmartin8/PyPortfolioOpt) — leveraging the CVXPY convex optimization library for solving quadratic programs.
- **Frontend/UI:** [Streamlit](https://streamlit.io/) — providing a reactive, data-dense interface for real-time visualization.
- **Data Pipeline:** [Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/) for vectorised financial calculations.
- **Simulations:** Custom **Monte Carlo** implementation projecting 1,000 parallel paths based on GBM (Geometric Brownian Motion) models.
- **Intelligence:** [Google GenAI (Gemini)](https://ai.google.dev/) for interpreting multi-dimensional trade data into qualitative summaries.

---

## 📉 Risk & Simulations

The system validates its optimized targets through a **Monte Carlo Simulation Engine**, which projects portfolio performance across 252 trading days. It computes probabilities for:
- **Value at Risk (VaR):** The 5th percentile "Worst Case" scenario.
- **Median Growth:** The expected pathway.
- **95th Percentile:** The optimistic market projection.
