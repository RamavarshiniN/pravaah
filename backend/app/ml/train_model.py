"""
Standalone script to (re)train the XGBoost demo model on synthetic data.
Run: python -m app.ml.train_model
NOTE: This is a clearly-labeled synthetic dataset for hackathon demonstration
only. No field-validated accuracy is claimed.
"""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from app.services.ml_predictor import _train_synthetic

if __name__ == "__main__":
    model = _train_synthetic()
    print("Model trained and saved to app/ml/model.joblib")
