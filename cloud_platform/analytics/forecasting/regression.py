"""Linear regression forecasting utilities."""
from __future__ import annotations

import logging
from typing import Iterable, List
import numpy as np

logger = logging.getLogger(__name__)


def forecast_with_linear_regression(history: Iterable[float], horizon_steps: int = 7) -> List[float]:
    """Generate forecast using simple linear regression.
    
    Args:
        history: Historical data points (time series values)
        horizon_steps: Number of future steps to forecast
        
    Returns:
        List of forecasted values
    """
    data = list(history)
    if not data or len(data) < 2:
        return [0.0] * horizon_steps
    
    try:
        # Create simple linear regression
        x = np.arange(len(data))
        y = np.array(data)
        
        # Calculate linear regression coefficients
        A = np.vstack([x, np.ones(len(x))]).T
        slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
        
        # Forecast future values
        future_x = np.arange(len(data), len(data) + horizon_steps)
        forecast = slope * future_x + intercept
        
        return list(forecast)
    except Exception as e:
        logger.error(f"Forecasting error: {e}")
        # Return last known value repeated
        return [data[-1]] * horizon_steps
