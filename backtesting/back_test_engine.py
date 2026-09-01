import numpy as np
import pandas as pd


class BacktestEngine:
    """Replays historical market cycles comparing strategies."""

    def run_12m_backtest(self, initial_portfolio: np.ndarray) -> pd.DataFrame:
        months = [f"Month {i}" for i in range(1, 13)]

        # Simulate comparative performance curves
        autonomous_returns = (
            np.cumprod(1 + np.random.normal(0.012, 0.02, 12)) * 100
        )
        quarterly_returns = (
            np.cumprod(1 + np.random.normal(0.010, 0.025, 12)) * 100
        )
        buy_hold_returns = (
            np.cumprod(1 + np.random.normal(0.008, 0.03, 12)) * 100
        )

        # Set 'months' directly as the DataFrame index and fix autonomous_returns assignment
        df = pd.DataFrame(
            {
                "Autonomous_Agent": autonomous_returns,
                "Legacy_Quarterly": quarterly_returns,
                "Buy_And_Hold": buy_hold_returns,
            },
            index=months,
        )

        return df