"""Test script for Explainability Engine verification."""

import os
import json
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from pathlib import Path
import pandas as pd
import numpy as np

from app.ml.feature_engineering import FeatureEngineer, NUMERICAL_FEATURE_COLS, CATEGORICAL_FEATURE_COLS
from app.ml.classifier import AttackClassifier
from app.ml.explainability import ExplainabilityEngine


def test_explainability() -> None:
    data_path = Path("data/train.csv")
    if not data_path.exists():
        print("data/train.csv not found, skipping CSV test.")
        return

    print("1. Loading dataset from data/train.csv...")
    df = pd.read_csv(data_path, nrows=1000)

    print("\n2. Running feature engineering...")
    fe = FeatureEngineer()
    X, _ = fe.fit_transform(df)
    
    # Generate the ordered list of feature names that matches the feature matrix X
    # Numerical features come first, then One-Hot Encoded categorical features
    feature_names = NUMERICAL_FEATURE_COLS.copy()
    feature_names.extend(fe.onehot_encoder.get_feature_names_out(CATEGORICAL_FEATURE_COLS))
    
    # We append the custom model scores as they are stacked horizontally in classifier.py
    feature_names.extend(["behavior_score", "sequence_score"])
    
    # Force inject multiple classes to train XGBoost
    class_names = [
        "Normal", "BruteForce", "CredentialStuffing", "ImpossibleTravel", 
        "DeviceSpoofing", "LateralMovement", "LowSlowExfiltration", "InsiderDrift"
    ]
    np.random.seed(42)
    y = np.random.randint(0, len(class_names), size=len(X))

    # Generate dummy Behavior and Sequence scores
    is_anomaly = (y != 0)
    behavior_scores = np.where(is_anomaly, np.random.uniform(60, 100, len(y)), np.random.uniform(0, 40, len(y)))
    sequence_scores = np.where(is_anomaly, np.random.uniform(50, 90, len(y)), np.random.uniform(10, 30, len(y)))

    print("\n3. Training XGBoost Attack Classifier...")
    classifier = AttackClassifier()
    classifier.fit(X, behavior_scores, sequence_scores, y, class_names)
    
    print("\n4. Initializing Explainability Engine (SHAP)...")
    explainer = ExplainabilityEngine(model=classifier.model, feature_names=feature_names)
    
    print("\n5. Testing explanations on simulated anomalies...")
    
    # Pick a few instances that were labeled as anomalies (y != 0)
    anomaly_indices = np.where(is_anomaly)[0][:3]
    
    for idx in anomaly_indices:
        # Prepare the exact feature vector that was fed into XGBoost
        X_instance_raw = X[idx]
        b_score = behavior_scores[idx]
        s_score = sequence_scores[idx]
        
        # Recreate the horizontal stack manually for the explainer
        X_instance = np.hstack([X_instance_raw, [b_score], [s_score]])
        
        predicted_class_index = int(classifier.model.predict(X_instance.reshape(1, -1))[0])
        predicted_class_name = classifier.classes_[predicted_class_index]
        
        explanation = explainer.explain_prediction(X_instance, predicted_class_index, top_n=3)
        
        print(f"\n--- Sample {idx} | Predicted: {predicted_class_name} ---")
        print("Machine Explanation (SHAP Values):")
        print(json.dumps(explanation["machine_explanation"], indent=2))
        print("Human Explanation (SOC Readout):")
        for reason in explanation["human_explanation"]:
            print(f"  {reason}")

    print("\nAll Explainability tests passed successfully! ✅")


if __name__ == "__main__":
    test_explainability()
