import numpy as np
import pandas as pd
from pypfopt import EfficientFrontier, objective_functions
from typing import Dict, List, Tuple, Any, Optional

def fetch_optimal_weights(mu: pd.Series, S: pd.DataFrame, regularization_gamma: float = 0.01, min_etf_weight: float = 0.60, etf_tickers: Optional[List[str]] = None) -> Dict[str, float]:
    """
    Calculate optimal portfolio weights using Mean-Variance Optimization,
    with L2 regularization and safety constraints for ETFs.
    
    Args:
        mu (pd.Series): Annualized expected returns
        S (pd.DataFrame): Annualized covariance matrix
        regularization_gamma (float): L2 regularization parameter
        min_etf_weight (float): Minimum total portfolio weight dedicated to ETFs
        etf_tickers (list): List of ticker strings that are considered ETFs
        
    Returns:
        dict: mapping of tickers to their optimized weights
    """
    
    # 1. Initialize EfficientFrontier with standard bounds (preventing shorting and over-concentration)
    ef = EfficientFrontier(mu, S, weight_bounds=(0.02, 0.40))  # Min 2%, Max 40% per single asset
    
    # 2. Add L2 regularization bridge extreme weights
    ef.add_objective(objective_functions.L2_reg, gamma=regularization_gamma)
    
    # 3. Add Custom Constraint: Safe ETF Allocation
    if etf_tickers and min_etf_weight > 0:
        # Find indices of ETFs in the covariance matrix (which matches mu's order)
        tickers = list(mu.index)
        etf_indices = [tickers.index(t) for t in etf_tickers if t in tickers]
        
        if etf_indices:
            # Add a constraint that the sum of weights for ETF assets must be >= min_etf_weight
            ef.add_constraint(lambda w: sum(w[i] for i in etf_indices) >= min_etf_weight)
            
    # 4. Generate the optimal weights using constraints natively supported by utility maximization (max_sharpe does a transformation that breaks custom bounding!)
    raw_weights = ef.max_quadratic_utility(risk_aversion=2.0)
    
    # Clean up minor rounding errors (e.g. 1e-17 becomes 0)
    cleaned_weights = ef.clean_weights()
    
    return cleaned_weights

def calculate_rebalance_trades(current_holdings: Dict[str, Dict[str, Any]], target_weights: Dict[str, float], current_prices: Dict[str, float], drift_threshold: float = 0.05) -> List[Dict[str, Any]]:
    """
    Compare current weights to target; suggest trades if drift > threshold.
    
    Args:
        current_holdings: dict {ticker: {'shares': int, 'cost_basis': float, 'account': str}}
        target_weights: dict {ticker: target_weight_float}
        current_prices: dict {ticker: price_float}
        drift_threshold: 5% default (rebalance if weight drift > 5%)
    
    Returns:
        trades: list of dicts {ticker, action, shares, reason, est_gain, account}
    """
    trades = []
    
    # Calculate the total portfolio value using only tickers we have current prices for
    portfolio_value = sum(
        current_holdings[t]['shares'] * current_prices[t] 
        for t in current_holdings if t in current_prices
    )
    
    for ticker in current_holdings:
        # Skip tickers we don't have pricing for
        if ticker not in current_prices:
            continue
        
        current_value = current_holdings[ticker]['shares'] * current_prices[ticker]
        current_weight = current_value / portfolio_value if portfolio_value > 0 else 0
        
        # Get target weight (default to 0 if not in target portfolio)
        target_weight = target_weights.get(ticker, 0)
        
        # Calculate the drift
        weight_diff = target_weight - current_weight
        
        # Check against the drift threshold
        if abs(weight_diff) > drift_threshold:
            
            # Find the new target value in dollars
            target_value = portfolio_value * target_weight
            value_to_trade = target_value - current_value
            
            # Determine exactly how many shares to buy or sell
            shares_to_trade = int(value_to_trade / current_prices[ticker])
            
            # If the trade ends up being less than 1 share, skip it
            if shares_to_trade == 0:
                continue
                
            action = 'BUY' if shares_to_trade > 0 else 'SELL'
            abs_shares = abs(shares_to_trade)
            
            # Estimate capital gains/losses (only applicable for SELLs)
            est_gain = 0
            if action == 'SELL':
                est_gain = (current_prices[ticker] - current_holdings[ticker]['cost_basis']) * abs_shares
                
            trades.append({
                'ticker': ticker,
                'action': action,
                'shares': abs_shares,
                'reason': f"Drift {abs(weight_diff)*100:.1f}% > {drift_threshold*100:.1f}% threshold",
                'est_gain': round(est_gain, 2),
                'current_weight': round(current_weight, 4),
                'target_weight': round(target_weight, 4),
                'account': current_holdings[ticker].get('account_type', 'UNKNOWN') # Important for tax!
            })
            
    return trades

def calculate_contribution_trades(current_holdings: Dict[str, Dict[str, Any]], target_weights: Dict[str, float], current_prices: Dict[str, float], new_cash: float, target_account: str = "TFSA") -> Tuple[List[Dict[str, Any]], float]:
    """
    Spends new cash to bridge the gap toward target weights, without selling any existing assets.
    Supports fractional shares to fully allocate capital.
    
    Args:
        current_holdings: dict {ticker: {'shares': int, ...}}
        target_weights: dict {ticker: target_weight_float}
        current_prices: dict {ticker: price_float}
        new_cash: float, the dollar amount to deposit
        target_account: str, the account type (e.g. TFSA, RRSP)
    
    Returns:
        trades: list of dicts with the generated BUY orders
        remaining_cash: float showing unallocated funds
    """
    trades = []
    
    portfolio_value = sum(
        current_holdings[t]['shares'] * current_prices[t] 
        for t in current_holdings if t in current_prices
    )
    
    total_target_value = portfolio_value + new_cash
    
    # Calculate deficits
    deficits = {}
    for ticker in target_weights:
        if ticker not in current_prices: continue
            
        current_val = current_holdings.get(ticker, {}).get('shares', 0) * current_prices[ticker]
        target_val = total_target_value * target_weights[ticker]
        
        deficit = target_val - current_val
        if deficit > 0:
            deficits[ticker] = deficit
            
    # Sort deficits descending
    sorted_tickers = sorted(deficits.keys(), key=lambda t: deficits[t], reverse=True)
    
    remaining_cash = new_cash
    
    for ticker in sorted_tickers:
        if remaining_cash <= 0: break
            
        alloc_dollars = min(deficits[ticker], remaining_cash)
        
        # Prevent weird super small fractional trades. Must be at least $1.00 worth of value
        if alloc_dollars < 1.00:
            continue
            
        # Fractional shares supported! Rounding to 4 decimal places for clean UI.
        shares = round(alloc_dollars / current_prices[ticker], 4)
        
        # Enforce a minimum practical share size to avoid "0.0001" edge cases
        if shares < 0.01:
            continue
        
        if shares > 0:
            trades.append({
                'ticker': ticker,
                'action': 'BUY',
                'shares': shares,
                'reason': f"Depositing cash to reach {target_weights[ticker]*100:.1f}% target",
                'est_gain': 0.0,
                'current_weight': round((current_holdings.get(ticker, {}).get('shares', 0) * current_prices[ticker]) / portfolio_value if portfolio_value > 0 else 0, 4),
                'target_weight': round(target_weights[ticker], 4),
                'account': target_account
            })
            remaining_cash -= (shares * current_prices[ticker])
            
    return trades, remaining_cash
