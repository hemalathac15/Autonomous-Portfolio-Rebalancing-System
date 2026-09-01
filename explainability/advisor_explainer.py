class AdvisorExplainer:
    """Generates quantitative breakdowns for Financial Advisors."""

    @staticmethod
    def generate_report(portfolio_id: str, current_w: list, target_w: list, trades: list, tax_impact: dict) -> str:
        report = f"""
        === ADVISOR REBALANCING SUMMARY ===
        Portfolio ID: {portfolio_id}

        Current Allocation vs Target:
        - Current: {[round(x, 3) for x in current_w]}
        - Target: {[round(x, 3) for x in target_w]}

        Execution Plan (Proposed Trades):
        - Trade Vector: {[round(x, 3) for x in trades]}

        Tax & Transaction  Metrics:
        - Est. Tax Liability: ₹{tax_impact.get('estimated_tax_liability', 0.0):,.2f}
        - Tax Efficiency Score: {tax_impact.get('tax_efficiency_score', 1.0):.2%}
        """
        return report.strip()