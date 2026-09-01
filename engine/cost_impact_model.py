import numpy as np

class TransactionCostModel:
    """Estimates trading costs using linear brokerage + non-linear square-root market impact."""

    def __init__(self, fixed_bps: float = 0.0010, impact_coeff: float = 0.05):
        self.fixed_bps = fixed_bps        # 10 bps fixed fee (brokerage + STT)
        self.impact_coeff = impact_coeff   # Market impact scaling factor

    def estimate_trade_cost(self, trade_amounts: np.ndarray, daily_volumes: np.ndarray) -> float:
        """
        Calculates total cost = Fixed Brokerage + Market Impact Cost (Square Root Model)
        Cost = sum(|trade| * fixed_bps) + sum(impact_coeff * price * volatility * sqrt(|trade| / daily_volume))
        """
        abs_trades = np.abs(trade_amounts)
        fixed_costs = np.sum(abs_trades * self.fixed_bps)

        # Avoid division by zero for assets with no volume
        volume_ratio = np.divide(abs_trades, daily_volumes, out=np.zeros_like(abs_trades), where=daily_volumes > 0)
        impact_costs = np.sum(self.impact_coeff * abs_trades * np.sqrt(volume_ratio))

        return float(fixed_costs + impact_costs)