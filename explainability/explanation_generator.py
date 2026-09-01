import numpy as np
from .advisor_explainer import AdvisorExplainer
from .client_explainer import ClientExplainer
from .compliance_explainer import ComplianceExplainer
from .counter_factual_generator import CounterfactualGenerator
from .shap_integration import ShapExplainer


class ExplanationGenerator:
    """Unified facade orchestrating explainable AI (XAI) outputs across

    SHAP attributions, persona-based narratives, and counterfactual analysis.
    """

    def __init__(self):
        self.client_explainer = ClientExplainer()
        self.advisor_explainer = AdvisorExplainer()
        self.compliance_explainer = ComplianceExplainer()
        self.counterfactual_gen = CounterfactualGenerator()
        self.shap_explainer = ShapExplainer()

    def generate_comprehensive_explanation(
        self,
        portfolio_id: str,
        current_weights: list,
        target_weights: list,
        proposed_trades: list,
        decision_data: dict = None,
        tax_data: dict = None,
        compliance_data: dict = None,
    ) -> dict:
        """Consolidates explanations across SHAP feature attributions,

        stakeholder-specific narratives, and counterfactual 'what-if' scenarios
        into a single payload.
        """
        # Ensure safe defaults for dictionaries and numpy arrays
        decision_data = decision_data or {}
        tax_data = tax_data or {}
        compliance_data = compliance_data or {}

        # Safely convert numpy arrays or iterables to standard Python lists
        c_weights = (
            current_weights.tolist()
            if isinstance(current_weights, np.ndarray)
            else list(current_weights)
        )
        t_weights = (
            target_weights.tolist()
            if isinstance(target_weights, np.ndarray)
            else list(target_weights)
        )
        p_trades = (
            proposed_trades.tolist()
            if isinstance(proposed_trades, np.ndarray)
            else list(proposed_trades)
        )

        # 1. SHAP Feature Attribution
        shap_summary = self.shap_explainer.compute_feature_attributions(
            current_weights=c_weights,
            target_weights=t_weights,
        )

        # 2. Persona Narratives
        client_text = self.client_explainer.generate_narrative(
            portfolio_id=portfolio_id,
            action_data=decision_data,  
        )

        advisor_report = self.advisor_explainer.generate_report(
            portfolio_id=portfolio_id,
            current_w=c_weights,
            target_w=t_weights,
            trades=p_trades,
            tax_impact=tax_data,
        )

        action_str = decision_data.get("action", "HOLD")
        compliance_log = self.compliance_explainer.generate_audit_log(
            portfolio_id=portfolio_id,
            decision_id=f"DEC_{portfolio_id}_{action_str}",
            audit_results=compliance_data,
        )

        # 3. Counterfactual Analysis (What if no rebalance occurs?)
        counterfactual_scenario = self.counterfactual_gen.generate_what_if(
            current_weights=c_weights,
            target_weights=t_weights,
        )

        return {
            "portfolio_id": portfolio_id,
            "shap_attributions": shap_summary,
            "narratives": {
                "client": client_text,
                "advisor": advisor_report,
                "compliance": compliance_log,
            },
            "counterfactual_analysis": counterfactual_scenario,
        }