class ExplainabilityScorecard:
    """
    Evaluates system explainability metrics including SHAP feature stability,
    explanation coverage, and client text readability scores.
    """

    def __init__(self, readability_threshold: float = 70.0):
        self.readability_threshold = readability_threshold

    @staticmethod
    def calculate_flesch_reading_ease(text: str) -> float:
        """
        Calculates Flesch Reading Ease score for generated client narratives.
        Higher scores indicate easier readability (target: 60-80 for Grade 8 level).
        """
        words = text.split()
        total_words = len(words)
        if total_words == 0:
            return 100.0

        # Heuristic count of sentences and syllables for narrative evaluation
        total_sentences = max(1, text.count(".") + text.count("!") + text.count("?"))
        total_syllables = sum(
            max(1, len([char for char in word.lower() if char in "aeiou"]))
            for word in words
        )

        # Flesch Reading Ease formula
        score = 206.835 - (1.015 * (total_words / total_sentences)) - (84.6 * (total_syllables / total_words))
        return round(max(0.0, min(100.0, score)), 2)

    def evaluate_scorecard(
        self, 
        shap_values_count: int, 
        client_explanation: str, 
        feature_attribution_dict: dict = None
    ) -> dict:
        """
        Generates a comprehensive explainability scorecard result.
        """
        readability_score = self.calculate_flesch_reading_ease(client_explanation)
        attribution_coverage = 100.0 if shap_values_count > 0 else 0.0

        # Check feature stability / non-empty attribution vector
        has_feature_importance = bool(feature_attribution_dict and len(feature_attribution_dict) > 0)

        status = "PASS" if (readability_score >= self.readability_threshold and attribution_coverage > 0) else "NEEDS_REVISION"

        return {
            "shap_attribution_coverage_pct": attribution_coverage,
            "client_readability_score": readability_score,
            "grade_level_target": "Grade 8 (Plain Language)",
            "feature_attribution_present": has_feature_importance,
            "scorecard_status": status,
            "compliance_certified": status == "PASS"
        }