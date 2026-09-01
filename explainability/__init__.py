"""
Explainability module initialization.
Exports explainers for clients, advisors, compliance teams, counterfactual analysis,
feature attribution (SHAP/LIME), and unified explanation generation.
"""

from .advisor_explainer import AdvisorExplainer
from .client_explainer import ClientExplainer
from .compliance_explainer import ComplianceExplainer
from .counter_factual_generator import CounterfactualGenerator
from .explanation_generator import ExplanationGenerator
from .lime_integration import LimeExplainer
from .shap_integration import ShapExplainer

__all__ = [
    "AdvisorExplainer",
    "ClientExplainer",
    "ComplianceExplainer",
    "CounterfactualGenerator",
    "ExplanationGenerator",
    "LimeExplainer",
    "ShapExplainer",
]