class InterventionClassifier:
    """Classifies trades into 4 Graduated Intervention Levels."""

    @staticmethod
    def classify(trade_magnitude: float, risk_breach: bool) -> str:
        if risk_breach:
            return "ESCALATION_REQUIRED"
        elif trade_magnitude > 0.15:
            return "APPROVAL_REQUIRED"
        elif trade_magnitude > 0.05:
            return "ADVISORY"
        else:
            return "INFORMATIONAL"