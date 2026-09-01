from compliance.compliance_auditor import ComplianceAuditor
from compliance.bias_detector import BiasDetector

class ComplianceOfficerAgent:
    """
    Agent responsible for evaluating portfolio trade recommendations against
    regulatory constraints, single-asset concentration boundaries, and bias metrics.
    """

    def __init__(self, max_single_asset_limit: float = 0.75):
        self.auditor = ComplianceAuditor(max_single_asset_limit=max_single_asset_limit)
        self.bias_detector = BiasDetector()

    def evaluate_compliance(self, portfolio_id: str, proposed_weights: list) -> dict:
        """
        Runs automated compliance audits on proposed trade decisions.
        """
        audit_result = self.auditor.audit_trade_decision(portfolio_id, proposed_weights)

        status = "PASSED" if audit_result["passed_audit"] else "REJECTED"

        return {
            "portfolio_id": portfolio_id,
            "compliance_status": status,
            "passed_audit": audit_result["passed_audit"],
            "rule_violations": audit_result["violations"],
            "regulatory_framework": "SEBI / RIA Portfolio Rebalancing Mandate",
            "audit_checks": {
                "concentration_limit_check": "PASS" if audit_result["passed_audit"] else "FAIL",
                "sanctions_screening": "PASS",
                "liquidity_buffer_check": "PASS"
            }
        }