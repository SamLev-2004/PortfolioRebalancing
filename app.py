import streamlit as st
import pandas as pd
from data_fetch import fetch_historical_data, compute_stats
from optimizer import fetch_optimal_weights, calculate_rebalance_trades, calculate_contribution_trades
from viz import plot_allocation_comparison, plot_efficient_frontier, plot_monte_carlo_simulations, plot_model_comparison
from monte_carlo import run_monte_carlo_simulation
from predictive_model import run_time_series_forecasts
import numpy as np

st.set_page_config(page_title="AI Rebalancer Prototype", layout="wide")

# -------- Sidebar: Portfolio Setup --------
st.sidebar.title("AI Portfolio Rebalancer")
st.sidebar.markdown("Upload your portfolio to generate optimized trade recommendations.")

uploaded_file = st.sidebar.file_uploader("Upload Portfolio (CSV/TSV)", type=['csv', 'tsv'])

with st.sidebar.expander("📄 View Expected CSV Format"):
    st.markdown("""
    Your CSV must contain these exact columns:
    ```csv
    ticker, shares, avg_cost, account_type
    AAPL, 50, 150.00, TFSA
    VFV.TO, 100, 110.50, RRSP
    ```
    """)

st.sidebar.markdown("---")
# Phase 2: SWAN Risk Toggle
swan_risk = st.sidebar.select_slider(
    "Sleep Well At Night (SWAN) Risk Tolerance",
    options=["Conservative", "Moderate", "Aggressive"],
    value="Moderate",
    help="Determines the minimum ETF allocation and maximum single-stock concentration."
)

# Map human risk to math constraints
if swan_risk == "Conservative":
    min_etf_weight = 0.80
    reg_gamma = 0.10  # Strict regularization, highly diversified
elif swan_risk == "Moderate":
    min_etf_weight = 0.60
    reg_gamma = 0.01  # Standard
else: # Aggressive
    min_etf_weight = 0.20
    reg_gamma = 0.001 # Let the AI make concentrated single-stock bets

st.sidebar.markdown("---")
new_deposit = st.sidebar.number_input(
    "Contribution Optimization: New Deposit ($)", 
    min_value=0.0, 
    value=0.0, 
    step=100.0,
    help="If greater than 0, the AI will build the portfolio toward optimal using ONLY this cash, avoiding any taxable sells."
)
target_account = st.sidebar.selectbox("Contribution Target Account", ["TFSA", "RRSP", "FHSA", "CASH/MARGIN"], index=0)


if uploaded_file is not None:
    # Infer separator safely
    try:
        portfolio_df = pd.read_csv(uploaded_file)
        # If it only parsed 1 column, it might be a TSV
        if len(portfolio_df.columns) == 1:
            uploaded_file.seek(0)
            portfolio_df = pd.read_csv(uploaded_file, sep='\t')
            
        portfolio_df.columns = portfolio_df.columns.str.strip().str.lower()
    except Exception as e:
        st.error(f"Could not read the uploaded portfolio file: {e}")
        st.stop()
        
    st.title("AI Portfolio Rebalancer")

    # -------- 1. Process Current Holdings --------
    current_holdings = {}
    for _, row in portfolio_df.iterrows():
        current_holdings[row['ticker']] = {
            'shares': row['shares'],
            'cost_basis': row['avg_cost'],
            'account_type': row['account_type']
        }
        
    tickers = list(current_holdings.keys())
    
    st.subheader(f"Analyzing {len(tickers)} Assets...")
    
    # Fetch all underlying financial data
    with st.spinner("Fetching historical market data from Yahoo Finance..."):
        tickers_data, current_prices, historical_prices_df = fetch_historical_data(tickers)
        
    if tickers_data is not None:
        
        # -------- 2. AI Optimization Engine --------
        try:
            mu, S = compute_stats(tickers_data)
        except Exception as e:
            st.error(f"Error computing portfolio statistics: {e}")
            st.stop()
        
        # Determine ETFs heuristically (or user input in a real product)
        # For prototype, we'll arbitrarily assume everything ending in 'EQT' or 'SP' or 'NQ' is an ETF
        etf_tickers = [t for t in tickers if 'EQT' in t or 'SP' in t or 'NQ' in t or 'VDY' in t]
        
        # Run Mathematical Optimization using SWAN Parameters
        optimal_weights = fetch_optimal_weights(
            mu, S, 
            regularization_gamma=reg_gamma, 
            min_etf_weight=min_etf_weight, 
            etf_tickers=etf_tickers
        )
        
        
        current_weights_pct = {}
        total_val = sum(current_holdings[t]['shares'] * current_prices.get(t,0) for t in tickers)
        for t in tickers:
            current_weights_pct[t] = (current_holdings[t]['shares'] * current_prices.get(t,0)) / total_val if total_val > 0 else 0
            
        # UI Tab Layout
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["AI Trades", "Risk / Return Math", "Current Input", "Monte Carlo Simulation", "Time-Series Forecast"])
        
        with tab1:
            # -------- 3. Rebalancer Output --------
            st.markdown(f"### Recommended Actions ({swan_risk} Setting)")
            
            if new_deposit > 0:
                trades, remaining_cash = calculate_contribution_trades(current_holdings, optimal_weights, current_prices, new_deposit, target_account)
                st.info(f"Contribution Mode Active: Spending ${new_deposit:,.2f} without selling any existing positions. Remaining unspent cash: **${remaining_cash:,.2f}**")
            else:
                drift = st.slider("Drift Threshold required to trigger trade (%)", 1, 15, 5, help="Only generate trades if an asset's weight drifts further than this threshold.") / 100.0
                trades = calculate_rebalance_trades(current_holdings, optimal_weights, current_prices, drift_threshold=drift)
            
            if len(trades) > 0:
                trade_df = pd.DataFrame(trades)
                
                # Highlight BUYS in green, SELLS in red using pandas styling
                def color_action(val):
                    color = '#27ae60' if val == 'BUY' else '#c0392b'
                    return f'color: {color}; font-weight: bold;'
                    
                # Format dataframe columns
                formatted_df = trade_df.style.applymap(color_action, subset=['action']) \
                                       .format({
                                           'est_gain': '${:,.2f}',
                                           'current_weight': '{:.2%}',
                                           'target_weight': '{:.2%}',
                                           'shares': '{:,.4f}' if new_deposit > 0 else '{:,.0f}'
                                       })
                    
                st.dataframe(formatted_df, use_container_width=True)
                

                
            else:
                st.success("Your portfolio is currently optimal and within the accepted drift thresholds!")

            st.plotly_chart(plot_allocation_comparison(current_weights_pct, optimal_weights), use_container_width=True)

        with tab2:
            st.markdown("### The Efficient Frontier")
            st.plotly_chart(plot_efficient_frontier(mu, S, optimal_weights), use_container_width=True)
            
        with tab3:
            st.markdown("### Processed Input Data")
            formatted_input_df = portfolio_df.style.format({'avg_cost': '${:,.2f}', 'shares': '{:,.0f}'})
            st.dataframe(formatted_input_df, use_container_width=True)
            
        with tab4:
            st.markdown("### 1-Year Future Projections")
            st.markdown("Using your AI Optimal Weights and historical volatility, we project 1000 simulated paths for your portfolio over the next 252 trading days.")
            
            with st.spinner("Running 1000 Monte Carlo permutations..."):
                simulated_paths = run_monte_carlo_simulation(total_val, optimal_weights, mu, S, days=252, num_sims=1000)
                
            st.plotly_chart(plot_monte_carlo_simulations(simulated_paths), use_container_width=True)
            
            # Additional metrics
            final_values = simulated_paths[-1, :]
            col1, col2, col3 = st.columns(3)
            col1.metric("Worst Case (5th %)", f"${np.percentile(final_values, 5):,.0f}")
            col2.metric("Expected (Median)", f"${np.median(final_values):,.0f}")
            col3.metric("Best Case (95th %)", f"${np.percentile(final_values, 95):,.0f}")
            
        with tab5:
            st.markdown("### Structural Time-Series Forecasting")
            st.markdown("Comparing ARIMA vs Exponential Smoothing (Holt-Winters) with configurable parameters and optional backtesting.")
            
            # -------- Model Tuning Controls --------
            with st.expander("⚙️ Model Tuning Parameters", expanded=True):
                tune_col1, tune_col2 = st.columns(2)
                
                with tune_col1:
                    st.markdown("**ARIMA Parameters**")
                    auto_arima = st.checkbox(
                        "🔍 Auto-Tune ARIMA", 
                        value=False,
                        help="Automatically search for the best (p, d, q) combination by minimizing AIC. This may take a few extra seconds."
                    )
                    
                    if not auto_arima:
                        arima_p = st.number_input(
                            "p (Autoregressive order)", min_value=0, max_value=5, value=1, step=1,
                            help="Number of lagged observations used in the model. Higher values capture longer-term dependencies in the data."
                        )
                        arima_d = st.number_input(
                            "d (Differencing order)", min_value=0, max_value=2, value=1, step=1,
                            help="Number of times the data is differenced to make it stationary. Use 1 for most financial time series."
                        )
                        arima_q = st.number_input(
                            "q (Moving Average order)", min_value=0, max_value=5, value=1, step=1,
                            help="Size of the moving average window. Controls how much past forecast errors influence the prediction."
                        )
                        arima_order = (arima_p, arima_d, arima_q)
                    else:
                        arima_order = (1, 1, 1)  # Default, will be overridden by auto search
                        
                with tune_col2:
                    st.markdown("**Exp. Smoothing Parameters**")
                    es_trend = st.selectbox(
                        "Trend Component", ["add", "mul", "none"],
                        index=0,
                        help="'add' = additive trend (linear growth). 'mul' = multiplicative trend (exponential growth). 'none' = no trend."
                    )
                    es_seasonal = st.selectbox(
                        "Seasonal Component", ["none", "add", "mul"],
                        index=0,
                        help="'add' = additive seasonality. 'mul' = multiplicative seasonality. 'none' = no seasonal pattern."
                    )
                    es_seasonal_periods = 5
                    if es_seasonal != "none":
                        es_seasonal_periods = st.number_input(
                            "Seasonal Period (trading days)", min_value=2, max_value=252, value=5, step=1,
                            help="The number of observations per seasonal cycle. 5 = weekly, 21 = monthly, 63 = quarterly, 252 = yearly in trading days."
                        )
                
                st.markdown("---")
                st.markdown("**Backtesting**")
                holdout_days = st.slider(
                    "Holdout Window (trading days)", 
                    min_value=0, max_value=120, value=0, step=5,
                    help="Hold out the last N trading days of real data to test model accuracy. Set to 0 to disable backtesting and only show future forecasts."
                )
            
            # -------- Run Models --------
            with st.spinner("Fitting Time-Series Models..."):
                forecast_results = run_time_series_forecasts(
                    historical_prices_df, optimal_weights, total_val,
                    forecast_days=30,
                    holdout_days=holdout_days,
                    arima_order=arima_order,
                    auto_tune_arima=auto_arima,
                    es_trend=es_trend,
                    es_seasonal=es_seasonal,
                    es_seasonal_periods=es_seasonal_periods
                )
                
            if forecast_results:
                # -------- Chart --------
                st.plotly_chart(plot_model_comparison(forecast_results), use_container_width=True)
                
                # -------- Auto ARIMA result --------
                if auto_arima:
                    best_order = forecast_results.get('best_arima_order', (1,1,1))
                    st.info(f"🔍 Auto-Tune selected ARIMA order: **({best_order[0]}, {best_order[1]}, {best_order[2]})**")
                
                # -------- End-Value Comparison --------
                es_final = forecast_results['es_forecast'][-1]
                arima_final = forecast_results['arima_forecast'][-1]
                
                colA, colB = st.columns(2)
                colA.metric(
                    "Exp. Smoothing 30-Day Target", 
                    f"${es_final:,.0f}", 
                    f"{(es_final - total_val) / total_val * 100:.2f}%"
                )
                colB.metric(
                    "ARIMA 30-Day Target", 
                    f"${arima_final:,.0f}", 
                    f"{(arima_final - total_val) / total_val * 100:.2f}%"
                )
                
                # -------- Backtest Metrics Table --------
                if forecast_results['metrics']:
                    st.markdown("---")
                    st.markdown("### 📊 Backtest Performance Metrics")
                    st.markdown(f"Models were trained on history up to {holdout_days} trading days ago, and then asked to predict the holdout window. Lower values = better fit.")
                    
                    metrics = forecast_results['metrics']
                    metrics_df = pd.DataFrame({
                        'Metric': ['MAE (Mean Abs. Error)', 'RMSE (Root Mean Sq. Error)', 'MAPE (Mean Abs. % Error)', 'AIC (Model Quality)'],
                        'Exp. Smoothing': [
                            f"${metrics['es']['MAE']:,.2f}",
                            f"${metrics['es']['RMSE']:,.2f}",
                            f"{metrics['es']['MAPE']:.2f}%",
                            str(metrics['es']['AIC'])
                        ],
                        'ARIMA': [
                            f"${metrics['arima']['MAE']:,.2f}",
                            f"${metrics['arima']['RMSE']:,.2f}",
                            f"{metrics['arima']['MAPE']:.2f}%",
                            str(metrics['arima']['AIC'])
                        ]
                    })
                    st.dataframe(metrics_df, use_container_width=True, hide_index=True)
                    
                    # Declare a winner
                    es_mape = metrics['es']['MAPE']
                    arima_mape = metrics['arima']['MAPE']
                    if es_mape < arima_mape:
                        st.success(f"✅ **Exponential Smoothing wins** on MAPE ({es_mape:.2f}% vs {arima_mape:.2f}%)")
                    elif arima_mape < es_mape:
                        st.success(f"✅ **ARIMA wins** on MAPE ({arima_mape:.2f}% vs {es_mape:.2f}%)")
                    else:
                        st.info("🤝 Both models performed equally on MAPE.")
            else:
                st.warning("Could not generate time-series models due to insufficient historical data.")
            
else:
    st.info("Awaiting Portfolio CSV Upload...")
