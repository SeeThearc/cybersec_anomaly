"""XGBoost classifier for Attack Classification.

Combines raw engineered features with Anomaly Behavior Score and Sequence Score
to classify events into Normal or 7 specific attack types. Outputs class
probabilities for explainability.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import joblib
import numpy as np
from xgboost import XGBClassifier


class AttackClassifier:
    """XGBoost model to classify events and provide confidence probabilities."""

    def __init__(self, random_state: int = 42) -> None:
        self.model = XGBClassifier(
            objective="multi:softprob",
            eval_metric="mlogloss",
            # XGBoost automatically handles missing/NaN natively
            random_state=random_state,
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            n_jobs=-1,
        )
        self.is_fitted: bool = False

        # Mapping numerical labels back to string class names.
        self.classes_: List[str] = []

    def _prepare_features(
        self, X: np.ndarray, behavior_scores: np.ndarray, sequence_scores: np.ndarray
    ) -> np.ndarray:
        """Appends behavior and sequence scores as new columns to the feature matrix."""
        # Ensure scores are column vectors
        b_scores = behavior_scores.reshape(-1, 1)
        s_scores = sequence_scores.reshape(-1, 1)
        return np.hstack([X, b_scores, s_scores])

    def fit(
        self,
        X: np.ndarray,
        behavior_scores: np.ndarray,
        sequence_scores: np.ndarray,
        y: np.ndarray,
        class_names: List[str],
    ) -> None:
        """Trains the XGBoost classifier on the combined feature matrix."""
        X_combined = self._prepare_features(X, behavior_scores, sequence_scores)
        self.classes_ = class_names
        
        print("Training XGBoost Attack Classifier...")
        self.model.fit(X_combined, y)
        self.is_fitted = True

    def predict(
        self, X: np.ndarray, behavior_scores: np.ndarray, sequence_scores: np.ndarray
    ) -> np.ndarray:
        """Predicts the top string class label for each sample."""
        if not self.is_fitted:
            raise RuntimeError("AttackClassifier is not fitted. Call fit() first.")

        X_combined = self._prepare_features(X, behavior_scores, sequence_scores)
        y_pred = self.model.predict(X_combined)

        # Map integer predictions to string class names
        return np.array([self.classes_[idx] for idx in y_pred])

    def predict_proba_dict(
        self, X: np.ndarray, behavior_scores: np.ndarray, sequence_scores: np.ndarray
    ) -> List[Dict[str, float]]:
        """Returns a list of dictionaries mapping class names to confidence probabilities."""
        if not self.is_fitted:
            raise RuntimeError("AttackClassifier is not fitted. Call fit() first.")

        X_combined = self._prepare_features(X, behavior_scores, sequence_scores)
        probas = self.model.predict_proba(X_combined)

        results = []
        for prob_row in probas:
            # Create dict of Class -> Probability (rounded to 4 decimal places)
            row_dict = {
                self.classes_[i]: round(float(prob_row[i]), 4)
                for i in range(len(self.classes_))
            }
            # Sort by highest probability first
            sorted_dict = dict(sorted(row_dict.items(), key=lambda item: item[1], reverse=True))
            results.append(sorted_dict)

        return results

    def save(self, model_dir: Path | str) -> None:
        """Saves the XGBoost model and configuration to disk."""
        model_dir = Path(model_dir)
        model_dir.mkdir(parents=True, exist_ok=True)

        state = {
            "model": self.model,
            "classes_": self.classes_,
            "is_fitted": self.is_fitted,
        }
        joblib.dump(state, model_dir / "attack_classifier.joblib")

    @classmethod
    def load(cls, model_dir: Path | str) -> AttackClassifier:
        """Loads the saved XGBoost model and configuration from disk."""
        model_dir = Path(model_dir)
        filepath = model_dir / "attack_classifier.joblib"

        if not filepath.exists():
            raise FileNotFoundError(f"Classifier model file not found at {filepath}")

        state = joblib.load(filepath)
        classifier = cls()
        classifier.model = state["model"]
        classifier.classes_ = state["classes_"]
        classifier.is_fitted = state["is_fitted"]

        return classifier
