from  explainability.client_explainer import ClientExplainer
from explainability.advisor_explainer import AdvisorExplainer
from explainability.compliance_explainer import ComplianceExplainer

class ExplanationWriterAgent:
    """
    Agent responsible for transalating technical portfolio rebalancing outputs
    into multi-audience explanations (Client, Advisor, and Compliance Audit).
    """

    def __init__(self):
        self.client_explainer = ClientExplainer()
        self.advisor_explainer = AdvisorExplainer()
        self.compliance_explainer = ComplianceExplainer()

    def generate_all_explanations(
        self, 
        portfolio_id: str,
        action_data: dict,
        tax_data: dict,
        compliance_data: dict
    ) -> dict:
        """
        Generates tailored narratives across all 3 stakeholder personas.
        """
        # Grade-8 plain language narrative for end-client
        client_narrative = self.client_explainer.generate_narrative(portfolio_id, action_data)

        # Quantitative breakdown for financial advisors
        advisor_report = self.advisor_explainer.generate_report(
            portfolio_id=portfolio_id,
            current_w=action_data.get("current_weights", []),
            target_w=action_data.get("target_weights", []),
            trades=action_data.get("trades_required", []),
            tax_impact=tax_data
        )

        # Exhaustive audit log for compliance teams
        decision_id = f"DEC_{portfolio_id}_{action_data.get('action', 'HOLD')}"
        compliance_log = self.compliance_explainer.generate_audit_log(
            portfolio_id=portfolio_id,
            decision_id=decision_id,
            audit_results=compliance_data
        )

        return{
            "client_explanation": client_narrative,
            "advisor_explanation": advisor_report,
            "compliance_audit_log": compliance_log
        }