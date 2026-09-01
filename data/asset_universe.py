import pandas as pd

class AssetUniverse:
    """Defines asset class universe metadata, risk free rates, and daily market volume snapshots."""

    ASSETS = {
        "Equity_IN": {"name": "Nifty 50 ETF", "expected_return": 0.12, "volatility": 0.16, "avg_daily_volume": 50000000.0},
        "Equity_INT": {"name": "S&P 500 ETF", "expected_return": 0.10, "volatility": 0.15, "avg_daily_volume": 80000000.0},
        "FixedIncome_IN": {"name": "India G-Sec 10Y", "expected_return": 0.07, "volatility": 0.04, "avg_daily_volume": 30000000.0},
        "FixedIncome_INT": {"name": "US Treasury 10Y", "expected_return": 0.04, "volatility": 0.05, "avg_daily_volume": 100000000.0},
        "Alternatives_Gold": {"name": "Gold BeES ETF", "expected_return": 0.08, "volatility": 0.12, "avg_daily_volume": 20000000.0},
        "Cash_Liquid": {"name": "Liquid Mutual Fund", "expected_return": 0.05, "volatility": 0.01, "avg_daily_volume": 200000000.0}
    }

    @classmethod
    def get_asset_dataframe(cls) -> pd.DataFrame:
        return pd.DataFrame.from_dict(cls.ASSETS, orient="index")