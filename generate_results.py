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

# Configure Risk Profiles
risk_profiles = {
    "Conservative": {"min_etf_weight": 0.80, "reg_gamma": 0.10},
    "Moderate":     {"min_etf_weight": 0.60, "reg_gamma": 0.01},
    "Aggressive":   {"min_etf_weight": 0.20, "reg_gamma": 0.001}
}

drift_threshold = 0.05

portfolios = [
    "stock portfolios/High Risk Portfolio.xlsx",
    "stock portfolios/Low Risk Portfolio.xlsx",
    "stock portfolios/Meme stock portfolio.xlsx",
    "portfolio.csv"
]
os.makedirs('results', exist_ok=True)

# List to accumulate all matrix grid data
matrix_data = []

# String to accumulate all detailed findings for the compiled report
compiled_markdown = "# Compiled AI Optimization Findings\n\nThis document contains the detailed fractional trades, constraints, and AI time-series forecasting metrics for every portfolio processed across all three (Conservative, Moderate, Aggressive) risk settings.\n\n---\n\n"

for p_path in portfolios:
    name = os.path.basename(p_path).split('.')[0]
    print(f"\n--- Processing {name} ---")
    
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
        
        total_val = sum(current_holdings[t]['shares'] * current_prices.get(t,0) for t in tickers if t in current_prices)
        
        # Now loop through each risk profile for this portfolio!
        for risk_name, risk_params in risk_profiles.items():
            print(f"  -> Running {risk_name} profile...")
            
            # Prevent infeasible constraints: if there are only a few ETFs, the max bounds per asset (0.40) might prevent reaching min_etf_weight
            dynamic_min_etf_weight = min(risk_params["min_etf_weight"], len(etf_tickers) * 0.40)
            
            optimal_weights = fetch_optimal_weights(
                mu, S, 
                regularization_gamma=risk_params["reg_gamma"], 
                min_etf_weight=dynamic_min_etf_weight, 
                etf_tickers=etf_tickers
            )
            
            # Calculate trades
            trades = calculate_rebalance_trades(current_holdings, optimal_weights, current_prices, drift_threshold)
            num_trades = len(trades)
            est_cap_gains = sum(t['est_gain'] for t in trades if 'est_gain' in t and t['action'] == 'SELL')
            
            # Calculate Optimal ETF %
            optimal_etf_pct = sum(optimal_weights.get(t, 0) for t in etf_tickers) * 100
            
            # Run time series forecasts
            forecast_results = run_time_series_forecasts(
                df_hist, optimal_weights, total_val, 
                forecast_days=30, holdout_days=0, auto_tune_arima=True
            )
            
            # Append to Compiled Markdown
            compiled_markdown += f"## Portfolio: {name} | Risk Profile: {risk_name}\n\n"
            compiled_markdown += f"**Total Initial Value:** ${total_val:,.2f} | **Target ETF Allocation:** {optimal_etf_pct:.1f}%\n\n"
            
            compiled_markdown += "### Initial vs Target Weights\n"
            for t in tickers:
                if t not in current_prices: continue
                cur_weight = (current_holdings[t]['shares'] * current_prices[t]) / total_val if total_val > 0 else 0
                tgt_weight = optimal_weights.get(t, 0)
                compiled_markdown += f"- **{t}**: Current: {cur_weight*100:.1f}% -> Target: {tgt_weight*100:.1f}%\n"
                
            compiled_markdown += "\n### Required Trades (5% Drift Threshold)\n"
            if not trades:
                compiled_markdown += "Portfolio is fully optimized. No trades required.\n"
            else:
                for t_dict in trades:
                    compiled_markdown += f"- **{t_dict['action']}** {t_dict['shares']} shares of {t_dict['ticker']} (Account: {t_dict['account']}, Expected Gain/Loss: ${t_dict['est_gain']:.2f})\n"
                    
            compiled_markdown += "\n### 30-Day Value Forecast (AI Model)\n"
            
            es_final = 0
            arima_final = 0
            if forecast_results:
                es_final = forecast_results['es_forecast'][-1]
                arima_final = forecast_results['arima_forecast'][-1]
                
                compiled_markdown += f"- Exponential Smoothing Target: **${es_final:,.0f}** ({((es_final - total_val) / total_val) * 100:.2f}%)\n"
                compiled_markdown += f"- Auto-ARIMA Target: **${arima_final:,.0f}** ({((arima_final - total_val) / total_val) * 100:.2f}%)\n"
                
                if 'best_arima_order' in forecast_results:
                    o = forecast_results['best_arima_order']
                    compiled_markdown += f"- *Best ARIMA Order Selected by AIC: (p={o[0]}, d={o[1]}, q={o[2]})*\n"
            else:
                compiled_markdown += "- Could not generate forecasts due to insufficient modeling data.\n"
                
            compiled_markdown += "\n---\n\n"
            
            # Add data mapping to Matrix List
            matrix_data.append({
                "Portfolio": name,
                "Risk Level": risk_name,
                "Total Value ($)": f"${total_val:,.2f}",
                "Target ETF %": f"{optimal_etf_pct:.1f}%",
                "Num Trades": num_trades,
                "Estimated Gains ($)": f"${est_cap_gains:,.2f}",
                "30-Day ES Forecast ($)": f"${es_final:,.0f}" if es_final else "N/A",
                "30-Day ARIMA Forecast ($)": f"${arima_final:,.0f}" if arima_final else "N/A"
            })
            
    except Exception as e:
        print(f"Error processing {name}: {e}")

# Save Compiled Report
with open("results/compiled_results.md", "w") as f:
    f.write(compiled_markdown)
print("Successfully saved compiled details to compiled_results.md!")

# Generate Master Grid
if matrix_data:
    print("\n--- Generating Master Matrix ---")
    df_matrix = pd.DataFrame(matrix_data)
    
    # Save as CSV
    df_matrix.to_csv("results/matrix_results.csv", index=False)
    
    # Save as Markdown Table
    with open("results/matrix_results.md", "w") as f:
        f.write("# Master Portfolio & Risk Matrix\n\n")
        f.write("This grid compares the AI optimizer's outputs across all portfolios and SWAN risk constraints.\n\n")
        f.write(df_matrix.to_markdown(index=False))
        
    print("Successfully generated matrix_results.csv and matrix_results.md!")
