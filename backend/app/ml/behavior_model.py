"""Behavior profiling using Isolation Forest and Autoencoder.

Learns normal user behavior profiles exclusively from normal log activity.
Generates an ensemble Behavior Anomaly Score on a 0 to 100 scale combining:
- Isolation Forest anomaly score (weight 0.6)
- Autoencoder reconstruction error (weight 0.4)
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Tuple

import joblib
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.neural_network import MLPRegressor


class AutoencoderModel:
    """Neural network autoencoder built using MLPRegressor for reconstruction error."""

    def __init__(self, hidden_layer_sizes: Tuple[int, ...] = (32, 16, 32), max_iter: int = 200, random_state: int = 42) -> None:
        self.model = MLPRegressor(
            hidden_layer_sizes=hidden_layer_sizes,
            activation="relu",
            solver="adam",
            max_iter=max_iter,
            random_state=random_state,
            early_stopping=True,
            validation_fraction=0.1,
            n_iter_no_change=10,
        )
        self.error_min: float = 0.0
        self.error_max: float = 1.0

    def fit(self, X: np.ndarray) -> None:
        """Train autoencoder on normal feature matrix X to reconstruct itself."""
        self.model.fit(X, X)
        X_pred = self.model.predict(X)
        errors = np.mean((X - X_pred) ** 2, axis=1)
        self.error_min = float(np.min(errors))
        # Use 99th percentile to prevent extreme outlier skew in scaling
        self.error_max = float(np.percentile(errors, 99))
        if self.error_max <= self.error_min:
            self.error_max = self.error_min + 1.0

    def predict_reconstruction_error(self, X: np.ndarray) -> np.ndarray:
        """Calculate raw Mean Squared Error (MSE) reconstruction loss."""
        X_pred = self.model.predict(X)
        return np.mean((X - X_pred) ** 2, axis=1)

    def predict_anomaly_score(self, X: np.ndarray) -> np.ndarray:
        """Calculate normalized autoencoder anomaly score in range [0.0, 1.0]."""
        errors = self.predict_reconstruction_error(X)
        scores = (errors - self.error_min) / (self.error_max - self.error_min)
        return np.clip(scores, 0.0, 1.0)


class BehaviorProfiler:
    """Ensemble behavior profiling model combining Isolation Forest and Autoencoder."""

    def __init__(self, if_weight: float = 0.6, ae_weight: float = 0.4, random_state: int = 42) -> None:
        self.if_weight = if_weight
        self.ae_weight = ae_weight
        self.random_state = random_state

        self.isolation_forest = IsolationForest(
            n_estimators=100,
            contamination=0.05,
            random_state=random_state,
            n_jobs=-1,
        )
        self.autoencoder = AutoencoderModel(random_state=random_state)

        self.if_score_min: float = -0.5
        self.if_score_max: float = 0.5
        self.is_fitted: bool = False

    def fit(self, X_normal: np.ndarray) -> None:
        """Train Isolation Forest and Autoencoder models on normal events only."""
        if len(X_normal) == 0:
            raise ValueError("Training dataset X_normal cannot be empty.")

        # 1. Fit Isolation Forest
        self.isolation_forest.fit(X_normal)
        dec_func = self.isolation_forest.decision_function(X_normal)
        self.if_score_min = float(np.min(dec_func))
        self.if_score_max = float(np.percentile(dec_func, 99))
        if self.if_score_max <= self.if_score_min:
            self.if_score_max = self.if_score_min + 1.0

        # 2. Fit Autoencoder
        self.autoencoder.fit(X_normal)

        self.is_fitted = True

    def predict_isolation_forest(self, X: np.ndarray) -> np.ndarray:
        """Predict Isolation Forest anomaly score in range [0.0, 1.0]."""
        if not self.is_fitted:
            raise RuntimeError("BehaviorProfiler must be fitted before predicting.")

        dec_func = self.isolation_forest.decision_function(X)
        # Decision function is lower for anomalies, higher for normal.
        # Invert scale so 0.0 = normal, 1.0 = highly anomalous.
        normalized = (self.if_score_max - dec_func) / (self.if_score_max - self.if_score_min)
        return np.clip(normalized, 0.0, 1.0)

    def predict_autoencoder(self, X: np.ndarray) -> np.ndarray:
        """Predict Autoencoder reconstruction error score in range [0.0, 1.0]."""
        if not self.is_fitted:
            raise RuntimeError("BehaviorProfiler must be fitted before predicting.")

        return self.autoencoder.predict_anomaly_score(X)

    def predict_behavior_score(self, X: np.ndarray) -> np.ndarray:
        """Calculate ensemble Behavior Score on 0 to 100 scale."""
        if_scores = self.predict_isolation_forest(X)
        ae_scores = self.predict_autoencoder(X)

        combined = (self.if_weight * if_scores) + (self.ae_weight * ae_scores)
        behavior_scores = combined * 100.0
        return np.clip(behavior_scores, 0.0, 100.0)

    def save(self, model_dir: Path | str) -> None:
        """Save fitted behavior models to disk inside trained_models/."""
        model_dir = Path(model_dir)
        model_dir.mkdir(parents=True, exist_ok=True)

        state = {
            "isolation_forest": self.isolation_forest,
            "autoencoder": self.autoencoder,
            "if_weight": self.if_weight,
            "ae_weight": self.ae_weight,
            "if_score_min": self.if_score_min,
            "if_score_max": self.if_score_max,
            "is_fitted": self.is_fitted,
        }
        joblib.dump(state, model_dir / "behavior_model.joblib")

    @classmethod
    def load(cls, model_dir: Path | str) -> BehaviorProfiler:
        """Load trained behavior models from disk."""
        model_dir = Path(model_dir)
        filepath = model_dir / "behavior_model.joblib"

        if not filepath.exists():
            raise FileNotFoundError(f"Behavior model file not found at {filepath}")

        state = joblib.load(filepath)
        profiler = cls(if_weight=state["if_weight"], ae_weight=state["ae_weight"])
        profiler.isolation_forest = state["isolation_forest"]
        profiler.autoencoder = state["autoencoder"]
        profiler.if_score_min = state["if_score_min"]
        profiler.if_score_max = state["if_score_max"]
        profiler.is_fitted = state["is_fitted"]
        return profiler
