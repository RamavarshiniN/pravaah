"""
Optional ML layer. Trains a small XGBoost classifier on synthetic,
clearly-labeled demo data if no model exists. Falls back silently
to None (rules-only) if xgboost/model unavailable — engine still works.
"""
import os
import numpy as np

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml", "model.joblib")
_model = None


def _train_synthetic():
    import pandas as pd
    from xgboost import XGBClassifier
    import joblib

    rng = np.random.default_rng(42)
    n = 2000
    water = rng.uniform(20, 200, n)
    r1h = rng.uniform(0, 60, n)
    r3h = r1h * rng.uniform(1.5, 3, n)
    r6f = rng.uniform(0, 80, n)
    rise = rng.uniform(-2, 30, n)
    hour = rng.integers(0, 24, n)
    monsoon = rng.integers(0, 2, n)

    label = np.where(
        (water >= 150) | ((rise >= 20) & (r6f >= 50)), 2,
        np.where((water >= 100) | (r1h >= 20) | (rise >= 8), 1, 0)
    )

    X = pd.DataFrame({
        "water": water, "r1h": r1h, "r3h": r3h, "r6f": r6f,
        "rise": rise, "hour": hour, "monsoon": monsoon
    })
    model = XGBClassifier(n_estimators=60, max_depth=3, eval_metric="mlogloss")
    model.fit(X, label)
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    return model


def get_model():
    global _model
    if _model is not None:
        return _model
    try:
        import joblib
        if os.path.exists(MODEL_PATH):
            _model = joblib.load(MODEL_PATH)
        else:
            _model = _train_synthetic()
    except Exception:
        _model = None
    return _model


def ml_probability(water, r1h, r3h, r6f, rise, hour=12, monsoon=1):
    """Returns probability of HIGH risk class, or None if model unavailable."""
    model = get_model()
    if model is None:
        return None
    import pandas as pd
    X = pd.DataFrame([{
        "water": water, "r1h": r1h, "r3h": r3h, "r6f": r6f,
        "rise": rise, "hour": hour, "monsoon": monsoon
    }])
    try:
        proba = model.predict_proba(X)[0]
        return float(proba[-1])  # probability of class 2 (HIGH)
    except Exception:
        return None
