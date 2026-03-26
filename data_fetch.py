import pandas as pd
import yfinance as yf
from sklearn.covariance import LedoitWolf
import streamlit as st
import numpy as np
from typing import Tuple, Dict, Optional, List

@st.cache_data(ttl=3600) # Cache for 1 hour
def fetch_historical_data(tickers: List[str], period: str = '2y') -> Tuple[Optional[pd.DataFrame], Optional[Dict[str, float]], Optional[pd.DataFrame]]:
    """
    Fetch adjusted close prices from Yahoo Finance.
    Returns: 
        returns: pd.DataFrame (dates x tickers) of daily returns
        current_prices: dict {ticker: latest_price}
        df: pd.DataFrame (dates x tickers) of raw closing prices
    """
    try:
        # Get the big chunk of data
        df = yf.download(tickers, period=period, auto_adjust=True)['Close']
        
        # 1. Calculate returns for the optimizer
        returns = df.pct_change().dropna()
        
        # 2. Extract strictly the latest prices for rebalancing!
        # Because df is already a DataFrame of actual prices, we can just grab the last row here too!
        current_prices = df.iloc[-1].to_dict()
        
        return returns, current_prices, df
        
    except Exception as e:
        st.error(f"Error fetching historical data from Yahoo Finance: {e}")
        return None, None, None

@st.cache_data(ttl=3600)
def compute_stats(tickers_data: pd.DataFrame) -> Tuple[pd.Series, pd.DataFrame]:
    """
    Compute annualized expected returns (μ) and covariance matrix (Σ).
    
    Args:
        tickers_data: pd.DataFrame of daily pct changes
    
    Returns:
        mu (pd.Series): Annualized expected return per asset
        S (pd.DataFrame): Annualized covariance matrix
    """
    if tickers_data is None or tickers_data.empty:
        raise ValueError("Cannot compute stats on empty ticker data")
        
    mu = tickers_data.mean() * 252 # 252 trading days
    lw = LedoitWolf()
    S_daily = lw.fit(tickers_data).covariance_

    S = pd.DataFrame(S_daily * 252, index=tickers_data.columns, columns=tickers_data.columns)
    return mu, S
