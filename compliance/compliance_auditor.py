import pandas as pd

class ComplianceAuditor:
    """Audits agent trade decisions against regulatory boundaries."""

    def __init__(self, max_single_asset_limit: float = 0.75):
        self.max_single_asset_limit = max_single_asset_limit

    def audit_trade_decision(self, portfolio_id: str, proposed_weights: list) -> dict:
        violations = []

        # Check single asset concentration rule
        for idx, weight in enumerate(proposed_weights):
            if weight > self.max_single_asset_limit:
                violations.append(f"Asset class {idx} exceeds max limit of {self.max_single_asset_limit:.0%}")

            return {
                "portfolio_id": portfolio_id,
                "passed_audit": len(violations) == 0,
                "violations": violations,
                "status": "APPROVED" if len(violations) == 0 else "REJECTED"
            }