import numpy as np
import pandas as pd
from lime.lime_tabular import LimeTabularExplainer


class LimeExplainer:
    """Generates local LIME explanations for individual portfolio rebalancing decisions."""

    def __init__(self, training_data: pd.DataFrame, feature_names: list = None):
        self.feature_names = feature_names or list(training_data.columns)
        self.explainer = LimeTabularExplainer(
            training_data=np.array(training_data),
            feature_names=self.feature_names,
            mode="regression",
        )

    def explain_instance(self, instance: pd.Series, predict_fn) -> dict:
        exp = self.explainer.explain_instance(
            data_row=instance.values, predict_fn=predict_fn
        )
        return dict(exp.as_list())


# Alias for backward compatibility
LIMEExplainer = LimeExplainer