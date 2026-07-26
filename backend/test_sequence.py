"""Test script for Sequence Learning verification."""

import os
# Disable TensorFlow logging for cleaner output
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

from pathlib import Path

import pandas as pd

from app.ml.feature_engineering import FeatureEngineer
from app.ml.sequence_model import SequenceProfiler


def test_sequence_profiling() -> None:
    data_path = Path("data/train.csv")
    if not data_path.exists():
        print("data/train.csv not found, skipping CSV test.")
        return

    print("Loading dataset from data/train.csv...")
    # Load enough data to get meaningful sequences per user
    df = pd.read_csv(data_path, nrows=10000)

    # 1. Feature Engineering and Sequence Tokenization
    print("Running feature engineering to tokenize sequences...")
    fe = FeatureEngineer()
    fe.fit_transform(df)

    seq_X, _ = fe.create_sequence_data(df, sequence_length=10)
    print(f"Extracted {len(seq_X)} sequences of length 10.")

    # Filter out a portion for training (e.g., normal sequences)
    # We will simulate the mask here since sequences overlap
    # In a real pipeline, we'd use only purely normal users' sequences for training.
    # For testing, we use the first 80%
    train_size = int(len(seq_X) * 0.8)
    seq_X_normal = seq_X[:train_size]
    
    if len(seq_X_normal) == 0:
        print("Not enough sequence data. Exiting.")
        return

    vocab_size = len(fe.action_tokenizer)
    print(f"Vocabulary Size (Unique Actions): {vocab_size}")

    # 2. Train Sequence Profiler (LSTM)
    print("Initializing and training LSTM Sequence Profiler...")
    profiler = SequenceProfiler(
        vocab_size=vocab_size,
        sequence_length=10,
        embedding_dim=16,
        lstm_units=32,
    )
    
    # Train for 2 epochs for quick testing
    profiler.fit(seq_X_normal, epochs=2, batch_size=32)
    print("Sequence Profiler trained successfully.")

    # 3. Predict on sample sequences
    test_seqs = seq_X[train_size:train_size + 100]
    if len(test_seqs) > 0:
        sequence_scores = profiler.predict_sequence_score(test_seqs)
        print(f"Sample Sequence Scores: Min={sequence_scores.min():.2f}, Max={sequence_scores.max():.2f}, Mean={sequence_scores.mean():.2f}")

    # 4. Save and Load Model
    save_dir = Path("trained_models")
    print("Saving sequence profiler model...")
    profiler.save(save_dir)
    assert (save_dir / "sequence_lstm.keras").exists(), "sequence_lstm.keras should be created"
    assert (save_dir / "sequence_params.json").exists(), "sequence_params.json should be created"

    print("Loading saved sequence profiler model...")
    loaded_profiler = SequenceProfiler.load(save_dir)
    assert loaded_profiler.model is not None, "Loaded profiler should have the model"

    if len(test_seqs) > 0:
        loaded_scores = loaded_profiler.predict_sequence_score(test_seqs[:50])
        assert len(loaded_scores) == min(50, len(test_seqs)), "Loaded prediction count mismatch"

    print("All Sequence Profiling tests passed successfully! ✅")


if __name__ == "__main__":
    test_sequence_profiling()
