"""Test script for Attack Classification verification."""

import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from pathlib import Path
import pandas as pd
import numpy as np

from app.ml.feature_engineering import FeatureEngineer
from app.ml.behavior_model import BehaviorProfiler
from app.ml.sequence_model import SequenceProfiler
from app.ml.classifier import AttackClassifier


def test_attack_classification() -> None:
    data_path = Path("data/train.csv")
    if not data_path.exists():
        print("data/train.csv not found, skipping CSV test.")
        return

    print("1. Loading dataset from data/train.csv...")
    df = pd.read_csv(data_path, nrows=5000)

    print("\n2. Running feature engineering...")
    fe = FeatureEngineer()
    X, _ = fe.fit_transform(df)
    
    # Force inject all 8 classes for the XGBoost unit test since the first 5000 rows
    # of the CSV are all "Normal" and XGBoost multi:softprob requires >= 2 classes.
    class_names = [
        "Normal", "BruteForce", "CredentialStuffing", "ImpossibleTravel", 
        "DeviceSpoofing", "LateralMovement", "LowSlowExfiltration", "InsiderDrift"
    ]
    y = np.random.randint(0, len(class_names), size=len(X))
    print(f"Force-injected {len(class_names)} classes for testing: {class_names}")

    # To run a full pipeline, we need behavior scores and sequence scores.
    # We will generate dummy scores for testing the classifier quickly.
    
    print("\n3. Generating simulated Behavior and Sequence scores for testing...")
    np.random.seed(42)
    # Give anomalies a higher fake score
    is_anomaly = (y != 0)  # 0 is Normal
    
    behavior_scores = np.where(is_anomaly, np.random.uniform(60, 100, len(y)), np.random.uniform(0, 40, len(y)))
    sequence_scores = np.where(is_anomaly, np.random.uniform(50, 90, len(y)), np.random.uniform(10, 30, len(y)))

    print("\n4. Initializing and training XGBoost Attack Classifier...")
    classifier = AttackClassifier()
    classifier.fit(X, behavior_scores, sequence_scores, y, class_names)
    print("Classifier trained successfully.")

    print("\n5. Testing predictions...")
    y_pred_labels = classifier.predict(X[:10], behavior_scores[:10], sequence_scores[:10])
    probas = classifier.predict_proba_dict(X[:10], behavior_scores[:10], sequence_scores[:10])
    
    for i in range(5):
        print(f"\nSample {i+1}:")
        print(f"  Predicted Label: {y_pred_labels[i]}")
        print(f"  Confidences: {probas[i]}")

    print("\n6. Saving and loading classifier model...")
    save_dir = Path("trained_models")
    classifier.save(save_dir)
    assert (save_dir / "attack_classifier.joblib").exists(), "attack_classifier.joblib should be created"

    loaded_classifier = AttackClassifier.load(save_dir)
    assert loaded_classifier.is_fitted is True, "Loaded classifier should be fitted"

    loaded_preds = loaded_classifier.predict(X[:5], behavior_scores[:5], sequence_scores[:5])
    assert len(loaded_preds) == 5, "Loaded prediction count mismatch"

    print("\nAll Attack Classification tests passed successfully! ✅")


if __name__ == "__main__":
    test_attack_classification()
