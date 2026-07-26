"""Test script for Behavior Profiling verification."""

from pathlib import Path
import pandas as pd
from app.ml.feature_engineering import FeatureEngineer
from app.ml.behavior_model import BehaviorProfiler


def test_behavior_profiling() -> None:
    data_path = Path("data/train.csv")
    if not data_path.exists():
        print("data/train.csv not found, skipping CSV test.")
        return

    print("Loading dataset from data/train.csv...")
    df = pd.read_csv(data_path, nrows=5000)

    # 1. Feature Engineering
    print("Running feature engineering...")
    fe = FeatureEngineer()
    X, _ = fe.fit_transform(df)

    # Filter normal events for training behavior profiler
    normal_mask = (df["label"] == "Normal").values
    X_normal = X[normal_mask]
    print(f"Normal events for training: {len(X_normal)} / {len(X)}")

    # 2. Train Behavior Profiler
    print("Training Behavior Profiler (Isolation Forest + Autoencoder)...")
    profiler = BehaviorProfiler()
    profiler.fit(X_normal)
    print("Behavior Profiler trained successfully.")

    # 3. Predict on sample normal & attack events
    if_scores = profiler.predict_isolation_forest(X)
    ae_scores = profiler.predict_autoencoder(X)
    behavior_scores = profiler.predict_behavior_score(X)

    print(f"Sample Behavior Scores: Min={behavior_scores.min():.2f}, Max={behavior_scores.max():.2f}, Mean={behavior_scores.mean():.2f}")

    # Compare mean behavior scores: Normal vs Attack events
    attack_mask = ~normal_mask
    if attack_mask.any():
        normal_avg_score = behavior_scores[normal_mask].mean()
        attack_avg_score = behavior_scores[attack_mask].mean()
        print(f"Average Normal Event Behavior Score: {normal_avg_score:.2f}")
        print(f"Average Attack Event Behavior Score: {attack_avg_score:.2f}")

    # 4. Save and Load Model
    save_dir = Path("trained_models")
    print("Saving behavior profiler model...")
    profiler.save(save_dir)
    assert (save_dir / "behavior_model.joblib").exists(), "behavior_model.joblib should be created"

    print("Loading saved behavior profiler model...")
    loaded_profiler = BehaviorProfiler.load(save_dir)
    assert loaded_profiler.is_fitted is True, "Loaded profiler should be fitted"

    loaded_scores = loaded_profiler.predict_behavior_score(X[:50])
    assert len(loaded_scores) == 50, "Loaded prediction count mismatch"

    print("All Behavior Profiling tests passed successfully! ✅")


if __name__ == "__main__":
    test_behavior_profiling()
