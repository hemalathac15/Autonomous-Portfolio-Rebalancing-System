import numpy as np
import pandas as pd
from typing  import Dict, List

class SyntheticPortfolioGenerator:
    """Generates synthetic client portfolios across 5 risk profiles and 6 asset classes."""

    RISK_PROFILES = {
        "Ultra-Conservative": np.array([0.05, 0.00, 0.60, 0.15, 0.05, 0.15]),
        "Conservative":       np.array([0.20, 0.05, 0.45, 0.10, 0.05, 0.15]),
        "Balanced":           np.array([0.40, 0.15, 0.25, 0.10, 0.05, 0.05]),
        "Aggressive":         np.array([0.55, 0.20, 0.15, 0.00, 0.05, 0.05]),
        "Ultra-Aggressive":   np.array([0.70, 0.20, 0.05, 0.00, 0.00, 0.05])
    }

    ASSET_CLASSES = [
        "Equity_IN", "Equity_INT", "FixedIncome_IN", 
        "FixedIncome_INT", "Alternatives_Gold", "Cash_Liquid"
    ]

    def generate_portfolios(self, num_portfolios: int = 50000, seed: int = 42) -> pd.DataFrame:
        np.random.seed(seed)
        profiles = list(self.RISK_PROFILES.keys())
        assigned_profiles = np.random.choice(profiles, size=num_portfolios)

        # Base AUM between 100,000 and 10,000,000
        aum = np.random.lognormal(mean=13, sigma=1.0, size=num_portfolios)

        holdings_matrix = np.zeros((num_portfolios, len(self.ASSET_CLASSES)))

        for i, profile in enumerate(assigned_profiles):
            target_weights = self.RISK_PROFILES[profile]
            #Add synthetic market drift (+/- 15% noise)
            noise = np.random.normal(0, 0.08, size=len(self.ASSET_CLASSES))
            drifted_weights = np.maximum(0, target_weights + noise)
            drifted_weights /= np.sum(drifted_weights)
            holdings_matrix[i] = drifted_weights * aum[i]

        df_cols = [f"holding_{asset}" for asset in self.ASSET_CLASSES]
        df = pd.DataFrame(holdings_matrix, columns=df_cols)
        df.insert(0, "portfolio_id", [f"PORT_{i:06d}" for i in range(num_portfolios)])
        df.insert(1, "risk_profile", assigned_profiles)
        df.insert(2, "total_aum", aum)

        return df