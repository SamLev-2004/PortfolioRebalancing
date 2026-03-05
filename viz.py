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
