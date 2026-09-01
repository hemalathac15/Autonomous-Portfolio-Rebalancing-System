import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from explainability.shap_integration import ShapExplainer


def test_shap_explainer_contributions():
    X = pd.DataFrame({"asset_1": [0.1, 0.2], "asset_2": [0.3, 0.4]})
    y = np.array([1.0, 2.0])

    model = RandomForestRegressor(n_estimators=5, random_state=42)
    model.fit(X, y)

    explainer = ShapExplainer(model=model)
    contributions = explainer.get_feature_contributions(X)

    assert isinstance(contributions, pd.DataFrame)
    assert contributions.shape == X.shape