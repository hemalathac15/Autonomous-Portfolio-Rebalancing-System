from dataclasses import dataclass, field
from typing import List

@dataclass
class ClientConstraintProfile:
    portfolio_id: str
    excluded_sectors: List[str] = field(default_factory=list) # e.g. ["Tobacco", "Weapons"] for ESG
    single_stock_lockup: List[str] = field(default_factory=list) # Single-stock ESOP lockups
    min_cash_buffer_pct: float = 0.02 # Minimum 2% cash liquidity constraint

class ConstraintEngine:
    """Applies client-specific overlays to optimization bound vectors."""

    @staticmethod
    def apply_cash_constraint(target_weights: list, min_cash_pct: float) -> list:
        adjusted = list(target_weights)
        if adjusted[-1] < min_cash_pct:
            delta = min_cash_pct - adjusted[-1]
            adjusted[-1] = min_cash_pct
            adjusted[0] = max(0.0, adjusted[0] - delta) # Reduce domestic equity to maintain cash
        return adjusted