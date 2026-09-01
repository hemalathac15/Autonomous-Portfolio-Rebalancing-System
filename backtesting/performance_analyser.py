import numpy as np
import pandas as pd

class PerformanceAnalyser:
    """
    Computes key portfolio metrics including Sharpe Ratio, Maximum Drawdown,
    Annualized Return, Volatility, Tracking Error, and Turnover.
    """

    def __init__(self, risk_free_rate: float = 0.05):
        self.risk_free_rate = risk_free_rate

    def calculate_annualized_return(self, returns_series: pd.Series, periods_per_year: int = 12) -> float:
        """Calculates annualized cumulative return."""
        compounded_growth = (1 + returns_series).prod()
        n_periods = len(returns_series)
        if n_periods == 0:
            return 0.0
        return float((compounded_growth ** (periods_per_year / n_periods)) - 1.0)

    def calculate_annualized_volatility(self, returns_series: pd.Series, periods_per_year: int = 12) -> float:
        """Calculates annualized standard deviation of returns."""
        if len(returns_series) < 2:
            return 0.0
        return float(returns_series.std() * np.sqrt(periods_per_year))

    def calculate_sharpe_ratio(self, returns_series: pd.Series, periods_per_year: int = 12) -> float:
        """Calculates annualized Sharpe Ratio."""
        ann_return = self.calculate_annualized_return(returns_series, periods_per_year)
        ann_vol = self.calculate_annualized_volatility(returns_series, periods_per_year)
        if ann_vol == 0:
            return 0.0
        return float((ann_return - self.risk_free_rate) / ann_vol)

    def calculate_max_drawdown(self, portfolio_values: pd.Series) -> float:
        """Calculates maximum peak-to-trough decline percentage."""
        if portfolio_values.empty:
            return 0.0
        peak = portfolio_values.cummax()
        drawdown = (portfolio_values - peak) / peak
        return float(drawdown.min())

    def calculate_tracking_error(self, portfolio_returns: pd.Series, benchmark_returns: pd.Series, periods_per_year: int = 12) -> float:
        """Calculates annualized tracking error against benchmark returns."""
        active_returns = portfolio_returns - benchmark_returns
        if len(active_returns) < 2:
            return 0.0
        return float(active_returns.std() * np.sqrt(periods_per_year))

    def generate_performance_summary(
        self, 
        portfolio_values: pd.Series, 
        benchmark_values: pd.Series = None, 
        turns_history: list = None
    ) -> dict:
      """
      Generates comprehensive analytics dictionary for dashboard views and reports.
      """
      returns = portfolio_values.pct_change().dropna()

      summary = {
          "annualized_return": round(self.calculate_annualized_return(returns), 4),
          "annualized_volatility": round(self.calculate_annualized_volatility(returns), 4),
          "sharpe_ratio": round(self.calculate_sharpe_ratio(returns), 2),
          "max_drawdown_pct": round(self.calculate_max_drawdown(portfolio_values) * 100, 2),
          "total_turnover_pct": round(float(np.sum(turns_history or [0.0])) * 100, 2)
      }
      if benchmark_values is not None:
          bm_returns = benchmark_values.pct_change().dropna()
          summary["tracking_error"] = round(self.calculate_tracking_error(returns, bm_returns), 4)
      return summary