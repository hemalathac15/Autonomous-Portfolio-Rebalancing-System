from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class TaxLot:
    lot_id: str
    asset_class: str
    units: float
    cost_basis: float
    purchase_date: datetime

class TaxLotTracker:
    """Tracks purchase lot for short-term vs long-term capital gains calculations."""

    def __init__(self):
        self.lots: List[TaxLot] = []

    def add_lot(self, lot: TaxLot):
        self.lots.append(lot)

    def calculate_unrealized_gains(self, asset_class: str, current_price: float, current_date: datetime) -> dict:
        stcg =  0.0
        ltcg = 0.0

        for lot in self.lots:
            if lot.asset_class != asset_class:
                continue

            holding_days = (current_date - lot.purchase_date).days
            gain = (current_price - lot.cost_basis) * lot.units

            #India tax rule: Equity > 365 days is LTCG
            is_long_term = holding_days > 365 if "Equity" in asset_class else holding_days > 1095

            if is_long_term:
                ltcg += gain
            else:
                stcg += gain

        return {"STCG": stcg, "LTCG": ltcg}