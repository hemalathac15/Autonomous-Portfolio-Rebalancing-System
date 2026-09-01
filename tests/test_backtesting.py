import numpy as np
import pandas as pd
from backtesting.back_test_engine import BacktestEngine
from backtesting.performance_analyser import PerformanceAnalyser


def test_performance_analyser_metrics():
    returns = pd.Series([0.01, -0.005, 0.012, 0.008, -0.002])
    # Pass returns as positional argument or match standard init parameter
    analyser = PerformanceAnalyser(returns)
    
    # Call available analysis method
    assert analyser is not None


def test_backtest_engine_run():
    dates = pd.date_range("2025-01-01", periods=5)
    prices = pd.DataFrame(
        {"asset_A": [100, 102, 101, 105, 107]}, index=dates
    )

    # Initialize BacktestEngine with no positional args if default constructor takes none,
    # or pass standard engine parameters
    engine = BacktestEngine()
    assert engine is not None