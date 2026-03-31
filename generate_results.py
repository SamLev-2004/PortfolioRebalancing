import os
import pandas as pd
import numpy as np
import sys
from unittest.mock import MagicMock

# Mock streamlit to prevent data_fetch from erroring or caching weirdly when run headless
mock_st = MagicMock()
mock_st.cache_data = lambda ttl=None: lambda f: f
sys.modules['streamlit'] = mock_st

from data_fetch import fetch_historical_data, compute_stats
from optimizer import fetch_optimal_weights, calculate_rebalance_trades
from predictive_model import run_time_series_forecasts

# Project configuration (Moderate Risk Profile Default)
min_etf_weight = 0.60
reg_gamma = 0.01
drift_threshold = 0.05

portfolios = [
    "stock portfolios/High Risk Portfolio.xlsx",
    "stock portfolios/Low Risk Portfolio.xlsx",
    "stock portfolios/Meme stock portfolio.xlsx",
    "portfolio.csv"
]
os.makedirs('results', exist_ok=True)

for p_path in portfolios:
    print(f"Processing {p_path}...")
    name = os.path.basename(p_path).split('.')[0]
    
    try:
        if p_path.endswith('.xlsx'):
            df = pd.read_excel(p_path)
        else:
            df = pd.read_csv(p_path)
            
        # Standardize cols
        df.columns = df.columns.str.strip().str.lower()
        
        current_holdings = {}
        for _, row in df.iterrows():
            current_holdings[row['ticker']] = {
                'shares': row['shares'],
                'cost_basis': row['avg_cost'],
                'account_type': row['account_type']
            }
            
        tickers = list(current_holdings.keys())
        
        returns, current_prices, df_hist = fetch_historical_data(tickers)
        
        if returns is None or df_hist is None:
            print(f"Failed to fetch historical data for {name}.")
            continue
            
        mu, S = compute_stats(returns)
        etf_tickers = [t for t in tickers if 'EQT' in t or 'SP' in t or 'NQ' in t or 'VDY' in t]
        
        # Prevent infeasible constraints: if there are only a few ETFs, the max bounds per asset (0.40) might prevent reaching min_etf_weight
        dynamic_min_etf_weight = min(min_etf_weight, len(etf_tickers) * 0.40)
        
        optimal_weights = fetch_optimal_weights(mu, S, regularization_gamma=reg_gamma, min_etf_weight=dynamic_min_etf_weight, etf_tickers=etf_tickers)
        
        # Calculate trades
        trades = calculate_rebalance_trades(current_holdings, optimal_weights, current_prices, drift_threshold)
        
        total_val = sum(current_holdings[t]['shares'] * current_prices.get(t,0) for t in tickers if t in current_prices)
        
        # Run time series forecasts
        forecast_results = run_time_series_forecasts(
            df_hist, optimal_weights, total_val, 
            forecast_days=30, holdout_days=0, auto_tune_arima=True
        )
        
        # Generate Output Markdown
        with open(f"results/{name}_results.md", "w") as f:
            f.write(f"# Portfolio Results: {name}\n\n")
            f.write(f"**Total Initial Value:** ${total_val:,.2f}\n\n")
            
            f.write("## Initial vs Target Weights\n")
            for t in tickers:
                if t not in current_prices: continue
                cur_weight = (current_holdings[t]['shares'] * current_prices[t]) / total_val if total_val > 0 else 0
                tgt_weight = optimal_weights.get(t, 0)
                f.write(f"- **{t}**: Current: {cur_weight*100:.1f}% -> Target: {tgt_weight*100:.1f}%\n")
                
            f.write("\n## Required Trades (5% Drift Threshold)\n")
            if not trades:
                f.write("Portfolio is fully optimized. No trades required.\n")
            else:
                for t_dict in trades:
                    f.write(f"- **{t_dict['action']}** {t_dict['shares']} shares of {t_dict['ticker']} (Account: {t_dict['account']}, Expected Gain/Loss: ${t_dict['est_gain']:.2f})\n")
                    
            f.write("\n## 30-Day Value Forecast (AI Model)\n")
            if forecast_results:
                es_final = forecast_results['es_forecast'][-1]
                arima_final = forecast_results['arima_forecast'][-1]
                
                f.write(f"- Exponential Smoothing Target: **${es_final:,.0f}** ({((es_final - total_val) / total_val) * 100:.2f}%)\n")
                f.write(f"- Auto-ARIMA Target: **${arima_final:,.0f}** ({((arima_final - total_val) / total_val) * 100:.2f}%)\n")
                
                if 'best_arima_order' in forecast_results:
                    o = forecast_results['best_arima_order']
                    f.write(f"- *Best ARIMA Order Selected by AIC: (p={o[0]}, d={o[1]}, q={o[2]})*\n")
            else:
                f.write("- Could not generate forecasts due to insufficient modeling data.\n")
                
        print(f"Successfully generated results for {name}")
    except Exception as e:
        print(f"Error processing {name}: {e}")
