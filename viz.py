import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_allocation_comparison(current_weights, target_weights):
    """
    Creates a side-by-side bar chart or donut charts comparing 
    current portfolio allocation vs AI's target allocation.
    """
    # Combine the data into a single DataFrame for Plotly
    df_current = pd.DataFrame(list(current_weights.items()), columns=['Ticker', 'Weight'])
    df_current['Type'] = 'Current Portfolio'
    
    df_target = pd.DataFrame(list(target_weights.items()), columns=['Ticker', 'Weight'])
    df_target['Type'] = 'AI Target'
    
    df = pd.concat([df_current, df_target])
    
    # We'll use a grouped bar chart
    fig = px.bar(
        df, 
        x='Ticker', 
        y='Weight', 
        color='Type', 
        barmode='group',
        title="Portfolio Allocation: Current vs. Optimal",
        labels={'Weight': 'Allocation %'},
        color_discrete_sequence=['#ff9f43', '#1dd1a1'] # App colors
    )
    
    # Format the y-axis to show percentages
    fig.update_layout(yaxis_tickformat='.1%')
    
    return fig

def plot_efficient_frontier(mu, S, optimal_weights=None):
    """
    Simulates random portfolios to visualize the Efficient Frontier scatter plot.
    """
    import numpy as np
    
    num_portfolios = 5000
    all_weights = np.zeros((num_portfolios, len(mu)))
    ret_arr = np.zeros(num_portfolios)
    vol_arr = np.zeros(num_portfolios)
    sharpe_arr = np.zeros(num_portfolios)

    for ind in range(num_portfolios):
        # Generate random weights
        weights = np.array(np.random.random(len(mu)))
        weights = weights / np.sum(weights)
        
        all_weights[ind, :] = weights
        
        # Expected Return
        ret_arr[ind] = np.sum((mu * weights))
        
        # Expected Volatility
        vol_arr[ind] = np.sqrt(np.dot(weights.T, np.dot(S, weights)))
        
        # Sharpe Ratio (Assuming 2% Risk Free Rate)
        sharpe_arr[ind] = (ret_arr[ind] - 0.02) / vol_arr[ind]

    # Plot the simulated random portfolios
    fig = px.scatter(
        x=vol_arr, y=ret_arr, color=sharpe_arr,
        labels={'x': 'Expected Volatility (Risk)', 'y': 'Expected Return', 'color': 'Sharpe Ratio'},
        title="Efficient Frontier (Risk vs. Reward)",
        color_continuous_scale='Viridis'
    )
    
    # If the user passed in the absolute mathematically optimal weights, plot it as a big red star
    if optimal_weights:
        opt_w = np.array([optimal_weights.get(t, 0) for t in mu.index])
        opt_ret = np.sum((mu * opt_w))
        opt_vol = np.sqrt(np.dot(opt_w.T, np.dot(S, opt_w)))
        
        fig.add_trace(go.Scatter(
            x=[opt_vol], y=[opt_ret],
            mode='markers',
            marker=dict(size=15, color='red', symbol='star'),
            name='Optimal AI Portfolio'
        ))
        
    fig.update_layout(yaxis_tickformat='.1%', xaxis_tickformat='.1%')
        
    return fig

def plot_monte_carlo_simulations(portfolio_paths, days=252):
    """
    Plots the Monte Carlo simulated paths.
    """
    import plotly.graph_objects as go
    import numpy as np
    
    num_days, num_sims = portfolio_paths.shape
    
    # We don't want to plot all 1000+ paths (too slow). We'll plot a random sample of 50.
    sample_size = min(50, num_sims)
    indices = np.random.choice(num_sims, sample_size, replace=False)
    
    fig = go.Figure()
    
    time_array = np.arange(num_days)
    
    for i in indices:
        fig.add_trace(go.Scatter(
            x=time_array,
            y=portfolio_paths[:, i],
            mode='lines',
            line=dict(color='lightgray', width=1),
            opacity=0.3,
            showlegend=False
        ))
        
    # Plot Median, 5th, and 95th percentiles
    median_path = np.median(portfolio_paths, axis=1)
    p5_path = np.percentile(portfolio_paths, 5, axis=1)
    p95_path = np.percentile(portfolio_paths, 95, axis=1)
    
    fig.add_trace(go.Scatter(x=time_array, y=median_path, mode='lines', line=dict(color='blue', width=3), name='Median (50th)'))
    fig.add_trace(go.Scatter(x=time_array, y=p5_path, mode='lines', line=dict(color='red', width=2, dash='dash'), name='Pessimistic (5th)'))
    fig.add_trace(go.Scatter(x=time_array, y=p95_path, mode='lines', line=dict(color='green', width=2, dash='dash'), name='Optimistic (95th)'))
    
    fig.update_layout(
        title="Monte Carlo 1-Year Portfolio Projection",
        xaxis_title="Trading Days",
        yaxis_title="Portfolio Value ($)",
        yaxis_tickprefix="$",
        yaxis_tickformat=",.0f"
    )
    
    return fig

def plot_model_comparison(forecast_results):
    """
    Plots the historical portfolio value alongside Exponential Smoothing and ARIMA forecasts.
    Supports optional backtest overlay when holdout data is present.
    """
    from datetime import timedelta
    
    fig = go.Figure()
    
    has_backtest = forecast_results['test_dates'] is not None
    
    if has_backtest:
        # Training data (muted)
        fig.add_trace(go.Scatter(
            x=forecast_results['train_dates'],
            y=forecast_results['train_values'],
            mode='lines',
            name='Training Data',
            line=dict(color='#666666', width=1.5)
        ))
        
        # Actual test data (ground truth - bright white)
        fig.add_trace(go.Scatter(
            x=forecast_results['test_dates'],
            y=forecast_results['test_values'],
            mode='lines',
            name='Actual (Holdout Truth)',
            line=dict(color='white', width=3)
        ))
        
        # Shaded backtest zone
        test_start = str(forecast_results['test_dates'][0])
        test_end = str(forecast_results['test_dates'][-1])
        fig.add_vrect(
            x0=test_start, x1=test_end,
            fillcolor="rgba(255, 200, 0, 0.06)",
            layer="below", line_width=0,
        )
        fig.add_annotation(
            x=test_start, y=1, yref="paper",
            text="Backtest Zone", showarrow=False,
            font=dict(size=11, color="rgba(255,200,0,0.7)"),
            xshift=50, yshift=-10
        )
        
        # ES Backtest prediction
        fig.add_trace(go.Scatter(
            x=forecast_results['test_dates'],
            y=forecast_results['es_backtest'],
            mode='lines',
            name='ES Backtest Prediction',
            line=dict(color='#00d2ff', width=2.5, dash='dot')
        ))
        
        # ARIMA Backtest prediction
        fig.add_trace(go.Scatter(
            x=forecast_results['test_dates'],
            y=forecast_results['arima_backtest'],
            mode='lines',
            name='ARIMA Backtest Prediction',
            line=dict(color='#ff6b6b', width=2.5, dash='dot')
        ))
    else:
        # No backtest — show full history
        fig.add_trace(go.Scatter(
            x=forecast_results['historical_dates'],
            y=forecast_results['historical_values'],
            mode='lines',
            name='Historical Portfolio Value',
            line=dict(color='#b0b0b0', width=2)
        ))
    
    # "Today" divider
    today_date = forecast_results['historical_dates'][-1]
    today_str = str(today_date)
    fig.add_vline(x=today_str, line_width=2, line_dash="dot", line_color="white")
    fig.add_annotation(
        x=today_str, y=1, yref="paper",
        text="Today", showarrow=False,
        font=dict(size=13, color="white"), yshift=10
    )
    
    # Shaded forecast zone
    future_dates = forecast_results['future_dates']
    fig.add_vrect(
        x0=today_str, x1=str(future_dates[-1]),
        fillcolor="rgba(255, 255, 255, 0.07)",
        layer="below", line_width=0,
    )
    fig.add_annotation(
        x=today_str, y=1, yref="paper",
        text="Forecast Horizon", showarrow=False,
        font=dict(size=11, color="rgba(255,255,255,0.5)"),
        xshift=60, yshift=-10
    )
    
    # Future forecast lines
    es_forecast = forecast_results['es_forecast']
    arima_forecast = forecast_results['arima_forecast']
    
    fig.add_trace(go.Scatter(
        x=future_dates, y=es_forecast,
        mode='lines+markers',
        name='Exp. Smoothing Forecast',
        line=dict(color='#00d2ff', width=4, dash='dash'),
        marker=dict(size=4, color='#00d2ff')
    ))
    
    fig.add_trace(go.Scatter(
        x=future_dates, y=arima_forecast,
        mode='lines+markers',
        name='ARIMA Forecast',
        line=dict(color='#ff6b6b', width=4, dash='dash'),
        marker=dict(size=4, color='#ff6b6b')
    ))
    
    # Endpoint markers
    fig.add_trace(go.Scatter(
        x=[future_dates[-1], future_dates[-1]],
        y=[es_forecast[-1], arima_forecast[-1]],
        mode='markers+text',
        marker=dict(size=12, color=['#00d2ff', '#ff6b6b'], symbol='diamond'),
        text=[f"${es_forecast[-1]:,.0f}", f"${arima_forecast[-1]:,.0f}"],
        textposition='top center',
        textfont=dict(size=11, color='white'),
        name='Targets', showlegend=False
    ))
    
    # Default zoom to last 6 months + forecast
    six_months_ago = today_date - timedelta(days=180)
    forecast_end = future_dates[-1] + timedelta(days=5)
    
    fig.update_layout(
        title="Predictive Modeling: ARIMA vs. Exponential Smoothing",
        xaxis_title="Date",
        yaxis_title="Portfolio Value ($)",
        yaxis_tickprefix="$",
        yaxis_tickformat=",.0f",
        hovermode="x unified",
        xaxis_range=[six_months_ago, forecast_end],
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig
