import numpy as np
import pandas as pd

def run_monte_carlo_simulation(portfolio_value, weights_dict, mu, S, days=252, num_sims=1000):
    """
    Simulate future portfolio paths using Geometric Brownian Motion (GBM).
    
    Args:
        portfolio_value (float): Starting dollar amount of the portfolio.
        weights_dict (dict): Dictionary of optimal weights (ticker: weight).
        mu (pd.Series): Annualized expected returns.
        S (pd.DataFrame): Annualized covariance matrix.
        days (int): Number of trading days to simulate (default 1 year).
        num_sims (int): Number of simulated paths.
        
    Returns:
        np.ndarray: Matrix of simulated portfolio values (days x num_sims).
    """
    tickers = list(weights_dict.keys())
    
    # Filter mu and S to match the tickers in weights_dict (in same order)
    mu_filtered = mu[tickers].values
    S_filtered = S.loc[tickers, tickers].values
    weights = np.array([weights_dict[t] for t in tickers])
    
    # Calculate expected portfolio return and volatility (annualized)
    port_mu = np.dot(weights.T, mu_filtered)
    port_vol = np.sqrt(np.dot(weights.T, np.dot(S_filtered, weights)))
    
    # Convert annualized stats to daily stats for the simulation
    daily_mu = port_mu / 252
    daily_vol = port_vol / np.sqrt(252)
    
    # Pre-allocate array for portfolio values
    portfolio_paths = np.zeros((days, num_sims))
    portfolio_paths[0] = portfolio_value
    
    # Generate all random shocks at once
    # Z ~ N(0,1)
    Z = np.random.normal(0, 1, size=(days - 1, num_sims))
    
    # Daily returns using GBM formula
    daily_returns = np.exp((daily_mu - 0.5 * daily_vol**2) + daily_vol * Z)
    
    # Cumulative product to get portfolio paths over the year
    portfolio_paths[1:] = portfolio_value * np.cumprod(daily_returns, axis=0)
    
    return portfolio_paths
