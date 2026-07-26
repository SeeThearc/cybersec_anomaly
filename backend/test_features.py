"""Test script for Feature Engineering pipeline verification."""

from pathlib import Path
import pandas as pd
from app.ml.feature_engineering import FeatureEngineer, NUMERICAL_FEATURE_COLS, CATEGORICAL_FEATURE_COLS


def test_feature_engineering() -> None:
    data_path = Path("data/train.csv")
    if not data_path.exists():
        print("data/train.csv not found, skipping CSV test.")
        return

    print("Loading sample data from data/train.csv...")
    df = pd.read_csv(data_path, nrows=1000)

    print(f"Loaded {len(df)} sample rows.")

    fe = FeatureEngineer()

    print("Extracting features...")
    df_feat = fe.extract_features(df)
    print(f"Features extracted successfully. Columns: {len(df_feat.columns)}")

    for col in NUMERICAL_FEATURE_COLS:
        assert col in df_feat.columns, f"Missing numerical feature column: {col}"

    for col in CATEGORICAL_FEATURE_COLS:
        assert col in df_feat.columns, f"Missing categorical feature column: {col}"

    print("Running fit_transform...")
    X, y = fe.fit_transform(df)
    print(f"Fit-transform successful. X shape: {X.shape}, y shape: {y.shape}")

    print("Running transform...")
    X_test, y_test = fe.transform(df.iloc[:100])
    print(f"Transform successful. X_test shape: {X_test.shape}, y_test shape: {y_test.shape}")

    print("Testing sequence data creation...")
    seq_X, seq_y = fe.create_sequence_data(df, sequence_length=5)
    print(f"Sequence creation successful. seq_X shape: {seq_X.shape}, seq_y shape: {seq_y.shape}")

    print("Testing preprocessor save & load...")
    save_dir = Path("trained_models")
    fe.save(save_dir)
    loaded_fe = FeatureEngineer.load(save_dir)
    assert loaded_fe.is_fitted is True, "Loaded preprocessor should be fitted"

    X_loaded, _ = loaded_fe.transform(df.iloc[:50])
    assert X_loaded.shape == (50, X.shape[1]), "Loaded transform shape mismatch"

    print("All Feature Engineering tests passed successfully! ✅")


if __name__ == "__main__":
    test_feature_engineering()
