import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings

warnings.filterwarnings("ignore")


def _compute_portfolio_series(historical_prices_df, target_weights, current_portfolio_value):
    """
    Internal helper: Build the historical portfolio value series 
    under the given optimal weights.
    """
    tickers = [t for t in target_weights.keys() if t in historical_prices_df.columns]
    
    if not tickers or historical_prices_df.empty:
        return None, None
        
    prices_subset = historical_prices_df[tickers]
    daily_returns = prices_subset.pct_change().dropna()
    
    weights_array = np.array([target_weights[t] for t in tickers])
    if weights_array.sum() > 0:
        weights_array = weights_array / weights_array.sum()
        
    port_daily_returns = daily_returns.dot(weights_array)
    cum_returns = (1 + port_daily_returns).cumprod()
    
    if len(cum_returns) == 0:
        return None, None
        
    historical_values = current_portfolio_value * (cum_returns / cum_returns.iloc[-1])
    return historical_values.index, historical_values.values


def _mape(y_true, y_pred):
    """Mean Absolute Percentage Error."""
    y_true = np.array(y_true, dtype=float)
    y_pred = np.array(y_pred, dtype=float)
    mask = y_true != 0
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100


def _fit_es(y_train, forecast_steps, trend='add', seasonal=None, seasonal_periods=None):
    """Fit Exponential Smoothing and return forecast array."""
    try:
        model = ExponentialSmoothing(
            y_train, 
            trend=trend if trend != 'none' else None, 
            seasonal=seasonal if seasonal != 'none' else None,
            seasonal_periods=seasonal_periods if seasonal != 'none' else None,
            initialization_method="estimated"
        )
        fit = model.fit()
        return fit.forecast(forecast_steps), fit.aic
    except:
        return np.full(forecast_steps, y_train[-1]), None


def _fit_arima(y_train, forecast_steps, order=(1, 1, 1)):
    """Fit ARIMA and return forecast array."""
    try:
        model = ARIMA(y_train, order=order)
        fit = model.fit()
        return fit.forecast(forecast_steps), fit.aic
    except:
        return np.full(forecast_steps, y_train[-1]), None


def _auto_arima(y_train, forecast_steps, max_p=3, max_d=2, max_q=3):
    """
    Simple grid-search auto ARIMA: finds the (p,d,q) with the lowest AIC.
    Returns forecasts, AIC, and the best order tuple.
    """
    best_aic = np.inf
    best_order = (1, 1, 1)
    best_forecast = np.full(forecast_steps, y_train[-1])
    
    for p in range(0, max_p + 1):
        for d in range(0, max_d + 1):
            for q in range(0, max_q + 1):
                try:
                    model = ARIMA(y_train, order=(p, d, q))
                    fit = model.fit()
                    if fit.aic < best_aic:
                        best_aic = fit.aic
                        best_order = (p, d, q)
                        best_forecast = fit.forecast(forecast_steps)
                except:
                    continue
                    
    return best_forecast, best_aic, best_order


def run_time_series_forecasts(
    historical_prices_df: pd.DataFrame,
    target_weights: dict,
    current_portfolio_value: float,
    forecast_days: int = 30,
    holdout_days: int = 0,
    arima_order: tuple = (1, 1, 1),
    auto_tune_arima: bool = False,
    es_trend: str = 'add',
    es_seasonal: str = 'none',
    es_seasonal_periods: int = 5
):
    """
    Build the historical portfolio value under optimal weights and forecast
    using ARIMA and Exponential Smoothing, with optional backtesting.
    
    Args:
        historical_prices_df: Raw closing prices (Date index, Ticker columns)
        target_weights: {ticker: optimal_weight}
        current_portfolio_value: Total portfolio dollar value
        forecast_days: Number of future days to predict
        holdout_days: If > 0, hold out the last N days for backtesting
        arima_order: (p, d, q) tuple for ARIMA
        auto_tune_arima: If True, grid-search for the best ARIMA order
        es_trend: 'add', 'mul', or 'none'
        es_seasonal: 'add', 'mul', or 'none'
        es_seasonal_periods: int, seasonal period length
        
    Returns:
        dict with historical data, forecasts, backtest results, and metrics.
    """
    dates, values = _compute_portfolio_series(
        historical_prices_df, target_weights, current_portfolio_value
    )
    
    if dates is None:
        return None
    
    # --- Train / Test Split ---
    if holdout_days > 0 and holdout_days < len(values) - 30:
        y_train = values[:-holdout_days]
        y_test = values[-holdout_days:]
        train_dates = dates[:-holdout_days]
        test_dates = dates[-holdout_days:]
    else:
        y_train = values
        y_test = None
        train_dates = dates
        test_dates = None
    
    # --- Fit Models ---
    # Exponential Smoothing
    es_backtest = None
    if y_test is not None:
        es_backtest, es_aic_bt = _fit_es(y_train, len(y_test), trend=es_trend, seasonal=es_seasonal, seasonal_periods=es_seasonal_periods)
    
    # For the actual future, always retrain on the FULL series
    es_forecast, es_aic = _fit_es(values, forecast_days, trend=es_trend, seasonal=es_seasonal, seasonal_periods=es_seasonal_periods)
    
    # ARIMA
    best_arima_order = arima_order
    arima_backtest = None
    if auto_tune_arima:
        if y_test is not None:
            arima_backtest, arima_aic_bt, best_arima_order = _auto_arima(y_train, len(y_test))
        arima_forecast, arima_aic, best_arima_order = _auto_arima(values, forecast_days)
    else:
        if y_test is not None:
            arima_backtest, arima_aic_bt = _fit_arima(y_train, len(y_test), order=arima_order)
        arima_forecast, arima_aic = _fit_arima(values, forecast_days, order=arima_order)
    
    # --- Generate future dates ---
    last_date = dates[-1]
    future_dates = pd.date_range(start=last_date, periods=forecast_days + 1, freq='B')[1:]
    
    # --- Compute Backtest Metrics ---
    metrics = None
    if y_test is not None and es_backtest is not None and arima_backtest is not None:
        metrics = {
            'es': {
                'MAE': round(mean_absolute_error(y_test, es_backtest), 2),
                'RMSE': round(np.sqrt(mean_squared_error(y_test, es_backtest)), 2),
                'MAPE': round(_mape(y_test, es_backtest), 2),
                'AIC': round(es_aic_bt, 2) if es_aic_bt else 'N/A'
            },
            'arima': {
                'MAE': round(mean_absolute_error(y_test, arima_backtest), 2),
                'RMSE': round(np.sqrt(mean_squared_error(y_test, arima_backtest)), 2),
                'MAPE': round(_mape(y_test, arima_backtest), 2),
                'AIC': round(arima_aic_bt, 2) if arima_aic_bt else 'N/A'
            }
        }
    
    return {
        'historical_dates': dates,
        'historical_values': values,
        'train_dates': train_dates,
        'train_values': y_train,
        'test_dates': test_dates,
        'test_values': y_test,
        'es_backtest': es_backtest,
        'arima_backtest': arima_backtest,
        'future_dates': future_dates,
        'es_forecast': es_forecast,
        'arima_forecast': arima_forecast,
        'metrics': metrics,
        'best_arima_order': best_arima_order
    }
