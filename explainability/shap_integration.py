from typing import Any, Dict, Optional
import numpy as np
import pandas as pd
import shap
from sklearn.ensemble import RandomForestRegressor


class ShapExplainer:
    """Computes Tree SHAP feature attributions for rebalancing triggers."""

    def __init__(self, model: Optional[RandomForestRegressor] = None) -> None:
        self.model = model
        self.explainer = (
            shap.TreeExplainer(model) if model is not None else None
        )

    def compute_feature_attributions(
        self, current_weights: list, target_weights: list
    ) -> dict:
        """Computes feature attributions from current and target weights payload.

        Falls back to exact drift attribution if tree model is not provided.
        """
        c_w = np.array(current_weights)
        t_w = np.array(target_weights)
        feature_names = [f"Asset_{i+1}" for i in range(len(c_w))]

        # If model and explainer are present, compute via Tree SHAP
        if self.explainer is not None:
            drift = np.abs(c_w - t_w)
            feature_df = pd.DataFrame([drift], columns=feature_names)
            contributions_df = self.get_feature_contributions(feature_df)
            shap_vals = contributions_df.iloc[0].to_dict()
            top_driver = max(shap_vals, key=shap_vals.get)
            return {
                "feature_names": feature_names,
                "shap_values": shap_vals,
                "top_driver": top_driver,
            }

        # Dynamic fallback attribution calculation when model is None
        drift_contributions = np.abs(c_w - t_w)
        total_drift = np.sum(drift_contributions)
        norm_attributions = (
            (drift_contributions / total_drift).tolist()
            if total_drift > 0
            else np.zeros_like(drift_contributions).tolist()
        )

        shap_dict = {
            f"Asset_{i+1}_Drift": round(float(val), 4)
            for i, val in enumerate(norm_attributions)
        }
        top_driver_idx = int(np.argmax(drift_contributions)) + 1

        return {
            "feature_names": feature_names,
            "shap_values": shap_dict,
            "top_driver": f"Asset_{top_driver_idx}_Drift",
        }

    def get_feature_contributions(
        self, feature_df: pd.DataFrame
    ) -> pd.DataFrame:
        """Calculates SHAP values for a given portfolio state dataframe."""
        if self.explainer is None:
            raise ValueError("Model and explainer are not initialized.")

        shap_values = self.explainer.shap_values(feature_df)

        # Handle list output for multi-output models or raw arrays
        if isinstance(shap_values, list):
            shap_matrix = np.array(shap_values[0])
        else:
            shap_matrix = np.array(shap_values)

        contributions = pd.DataFrame(
            shap_matrix, columns=feature_df.columns, index=feature_df.index
        )
        return contributions


# Alias for backward compatibility
ExplainabilityEngine = ShapExplainer