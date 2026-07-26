"""LSTM model for sequence learning of user behavior.

Learns normal sequences of actions using a Keras LSTM model.
The model predicts the next action in a sequence. Sequences that are highly
unpredictable yield a high categorical cross-entropy loss, resulting in a high
Sequence Anomaly Score (0 to 100 scale).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import LSTM, Dense, Dropout, Embedding, Input
from tensorflow.keras.losses import SparseCategoricalCrossentropy
from tensorflow.keras.models import Sequential, load_model


class SequenceProfiler:
    """LSTM model to learn normal sequences of user actions and detect anomalies."""

    def __init__(
        self,
        vocab_size: int,
        sequence_length: int = 10,
        embedding_dim: int = 32,
        lstm_units: int = 64,
    ) -> None:
        self.vocab_size = vocab_size
        self.sequence_length = sequence_length
        self.embedding_dim = embedding_dim
        self.lstm_units = lstm_units
        self.model: Optional[Sequential] = None

        # Boundaries used to scale prediction loss to a 0-100 anomaly score
        self.loss_min: float = 0.0
        self.loss_max: float = 1.0

    def build_model(self) -> None:
        """Builds and compiles the LSTM Keras model."""
        self.model = Sequential(
            [
                Input(shape=(self.sequence_length - 1,)),
                Embedding(
                    input_dim=self.vocab_size + 1,
                    output_dim=self.embedding_dim,
                ),
                LSTM(self.lstm_units, return_sequences=False),
                Dropout(0.2),
                Dense(self.vocab_size + 1, activation="softmax"),
            ]
        )

        self.model.compile(
            optimizer="adam",
            loss=SparseCategoricalCrossentropy(),
            metrics=["accuracy"],
        )

    def fit(self, seq_X_normal: np.ndarray, epochs: int = 5, batch_size: int = 64) -> None:
        """Trains the LSTM on normal sequences (predicting the next token)."""
        if self.model is None:
            self.build_model()

        # We take a sequence of length N and split it into:
        # X: first N-1 tokens
        # y: the Nth token (target to predict)
        X = seq_X_normal[:, :-1]
        y = seq_X_normal[:, -1]

        # Fit the model
        print("Training LSTM Sequence Model...")
        self.model.fit(
            X, y, epochs=epochs, batch_size=batch_size, validation_split=0.1, verbose=1
        )

        # Calculate loss boundaries for anomaly scoring
        predictions = self.model.predict(X, batch_size=batch_size, verbose=0)

        # Calculate cross-entropy loss for each sample: -log(P(y_true))
        losses = -np.log(predictions[np.arange(len(y)), y] + 1e-10)

        self.loss_min = float(np.min(losses))
        self.loss_max = float(np.percentile(losses, 99))
        if self.loss_max <= self.loss_min:
            self.loss_max = self.loss_min + 1.0

    def predict_sequence_score(self, seq_X: np.ndarray) -> np.ndarray:
        """
        Predicts anomaly score for sequences.
        Returns a score from 0 to 100 (100 = highly anomalous).
        """
        if self.model is None:
            raise RuntimeError("SequenceProfiler is not fitted. Call fit() first.")

        X = seq_X[:, :-1]
        y = seq_X[:, -1]

        predictions = self.model.predict(X, batch_size=128, verbose=0)
        losses = -np.log(predictions[np.arange(len(y)), y] + 1e-10)

        # Normalize losses
        normalized = (losses - self.loss_min) / (self.loss_max - self.loss_min)
        scores = np.clip(normalized, 0.0, 1.0) * 100.0
        return scores

    def save(self, model_dir: Path | str) -> None:
        """Saves the Keras model and parameters to disk."""
        model_dir = Path(model_dir)
        model_dir.mkdir(parents=True, exist_ok=True)

        if self.model is not None:
            self.model.save(model_dir / "sequence_lstm.keras")

        params = {
            "vocab_size": self.vocab_size,
            "sequence_length": self.sequence_length,
            "embedding_dim": self.embedding_dim,
            "lstm_units": self.lstm_units,
            "loss_min": self.loss_min,
            "loss_max": self.loss_max,
        }

        with open(model_dir / "sequence_params.json", "w") as f:
            json.dump(params, f, indent=4)

    @classmethod
    def load(cls, model_dir: Path | str) -> SequenceProfiler:
        """Loads the saved Keras model and parameters from disk."""
        model_dir = Path(model_dir)
        params_path = model_dir / "sequence_params.json"

        if not params_path.exists():
            raise FileNotFoundError(f"Sequence parameters not found at {params_path}")

        with open(params_path, "r") as f:
            params = json.load(f)

        profiler = cls(
            vocab_size=params["vocab_size"],
            sequence_length=params["sequence_length"],
            embedding_dim=params["embedding_dim"],
            lstm_units=params["lstm_units"],
        )
        profiler.loss_min = params["loss_min"]
        profiler.loss_max = params["loss_max"]

        model_path = model_dir / "sequence_lstm.keras"
        if model_path.exists():
            profiler.model = load_model(model_path)

        return profiler
