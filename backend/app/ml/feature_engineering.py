"""Feature engineering pipeline for raw security logs.

Converts raw enterprise event logs into structured feature matrices
for behavior profiling (Isolation Forest, Autoencoder), sequence models (LSTM),
and attack classification (XGBoost).
"""

from __future__ import annotations

import math
import os
from pathlib import Path
from typing import Any, Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, OneHotEncoder, StandardScaler

# ── Geo Coordinates for Distance Calculation ──────────────────────────

COUNTRY_COORDINATES: dict[str, Tuple[float, float]] = {
    "India": (20.5937, 78.9629),
    "USA": (37.0902, -95.7129),
    "UK": (55.3781, -3.4360),
    "Germany": (51.1657, 10.4515),
    "Australia": (-25.2744, 133.7751),
    "Canada": (56.1304, -106.3468),
    "Singapore": (1.3521, 103.8198),
    "Japan": (36.2048, 138.2529),
}

SENSITIVE_RESOURCES: set[str] = {
    "Payroll", "Admin Console", "Database", "HR Portal",
    "Security Console", "Active Directory", "SAP", "Finance Portal",
    "Server Dashboard", "Firewall Console", "Forensics Tool",
}

RESOURCE_CATEGORIES: dict[str, str] = {
    "Authentication": "Auth",
    "Login": "Auth",
    "Logout": "Auth",
    "Payroll": "Financial",
    "Finance Portal": "Financial",
    "SAP": "Financial",
    "Expense System": "Financial",
    "Tax Portal": "Financial",
    "HR Portal": "HR",
    "Recruitment System": "HR",
    "Benefits Portal": "HR",
    "Employee Directory": "HR",
    "Training Platform": "HR",
    "GitHub": "Engineering",
    "Jira": "Engineering",
    "Confluence": "Engineering",
    "Jenkins": "Engineering",
    "AWS Console": "Engineering",
    "VS Code Server": "Engineering",
    "Docker Hub": "Engineering",
    "Admin Console": "Admin",
    "Active Directory": "Admin",
    "Server Dashboard": "Admin",
    "Network Monitor": "Admin",
    "Firewall Console": "Admin",
    "SIEM Dashboard": "Security",
    "Threat Intel": "Security",
    "Forensics Tool": "Security",
    "Vulnerability Scanner": "Security",
    "Security Console": "Security",
    "Endpoint Protection": "Security",
}

# Numerical feature columns used for ML training/prediction
NUMERICAL_FEATURE_COLS: list[str] = [
    "hour",
    "day_of_week",
    "day_of_month",
    "month",
    "is_weekend",
    "is_working_hours",
    "session_duration",
    "time_since_prev_login",
    "failed_attempts",
    "success_after_failures",
    "attempts_per_minute",
    "device_changed",
    "known_device",
    "country_changed",
    "travel_distance_km",
    "travel_speed_kmh",
    "impossible_travel_flag",
    "bytes_transferred",
    "user_avg_login_hour",
    "user_avg_session_duration",
    "user_avg_bytes_transferred",
    "resource_diversity",
    "unique_ip_count",
    "is_vpn",
    "is_private_network",
    "is_sensitive_resource",
    "first_time_access",
    "resource_access_frequency",
]

CATEGORICAL_FEATURE_COLS: list[str] = [
    "authentication_method",
    "action",
    "login_status",
    "resource_category",
]


def haversine_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """Calculate the great-circle distance between two points in km."""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    r = 6371.0  # Earth radius in km

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return r * c


class FeatureEngineer:
    """Feature engineering pipeline for raw security events."""

    def __init__(self) -> None:
        self.scaler = StandardScaler()
        self.onehot_encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        self.label_encoder = LabelEncoder()
        self.action_tokenizer: dict[str, int] = {}
        self.is_fitted: bool = False

    def extract_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extract all engineered features from raw log events DataFrame."""
        df = df.copy()

        # Ensure timestamp is datetime
        if not pd.api.types.is_datetime64_any_dtype(df["timestamp"]):
            df["timestamp"] = pd.to_datetime(df["timestamp"])

        # Sort by user and timestamp for temporal feature calculations
        df = df.sort_values(by=["user_id", "timestamp"]).reset_index(drop=True)

        # ── 1. Time Features ──────────────────────────────────────────
        df["hour"] = df["timestamp"].dt.hour
        df["day_of_week"] = df["timestamp"].dt.dayofweek
        df["day_of_month"] = df["timestamp"].dt.day
        df["month"] = df["timestamp"].dt.month
        df["is_weekend"] = df["day_of_week"].apply(lambda d: 1 if d >= 5 else 0)
        df["is_working_hours"] = df["hour"].apply(lambda h: 1 if 8 <= h <= 18 else 0)
        df["session_duration"] = df["session_duration"].fillna(0).astype(float)

        # Time since previous login per user
        login_events = df[df["action"] == "Login"].copy()
        login_events["prev_login_time"] = login_events.groupby("user_id")["timestamp"].shift(1)
        df["prev_login_time"] = login_events["prev_login_time"]
        df["prev_login_time"] = df.groupby("user_id")["prev_login_time"].ffill()

        df["time_since_prev_login"] = (
            (df["timestamp"] - df["prev_login_time"]).dt.total_seconds().fillna(86400.0)
        )
        df["time_since_prev_login"] = df["time_since_prev_login"].clip(lower=0.0)
        df.drop(columns=["prev_login_time"], errors="ignore", inplace=True)

        # ── 2. Authentication Features ────────────────────────────────
        df["failed_attempts"] = df["failed_attempts"].fillna(0).astype(float)
        df["success_after_failures"] = (
            (df["login_status"] == "success") & (df["failed_attempts"] > 0)
        ).astype(int)

        # Attempts per minute
        df["attempts_per_minute"] = df.groupby(["user_id", pd.Grouper(key="timestamp", freq="1min")])[
            "id" if "id" in df.columns else "user_id"
        ].transform("count").fillna(1).astype(float)

        # ── 3. Device Features ────────────────────────────────────────
        df["prev_device_id"] = df.groupby("user_id")["device_id"].shift(1)
        df["device_changed"] = (
            (df["device_id"].notna()) &
            (df["prev_device_id"].notna()) &
            (df["device_id"] != df["prev_device_id"])
        ).astype(int)
        df.drop(columns=["prev_device_id"], errors="ignore", inplace=True)

        df["known_device"] = df["device_id"].apply(lambda d: 1 if pd.notna(d) and d != "" else 0)

        # ── 4. Geo Features ───────────────────────────────────────────
        df["prev_country"] = df.groupby("user_id")["country"].shift(1)
        df["country_changed"] = (
            (df["prev_country"].notna()) & (df["country"] != df["prev_country"])
        ).astype(int)

        df["prev_timestamp"] = df.groupby("user_id")["timestamp"].shift(1)
        df["time_delta_hours"] = (
            (df["timestamp"] - df["prev_timestamp"]).dt.total_seconds() / 3600.0
        ).fillna(24.0).clip(lower=0.001)

        # Distance & Speed
        def calculate_geo_metrics(row: pd.Series) -> Tuple[float, float, int]:
            curr_c = row["country"]
            prev_c = row["prev_country"]
            delta_h = row["time_delta_hours"]

            if pd.isna(prev_c) or curr_c == prev_c or curr_c not in COUNTRY_COORDINATES or prev_c not in COUNTRY_COORDINATES:
                return 0.0, 0.0, 0

            dist = haversine_distance(COUNTRY_COORDINATES[prev_c], COUNTRY_COORDINATES[curr_c])
            speed = dist / delta_h
            impossible = 1 if (speed > 800.0 and dist > 500.0) else 0
            return dist, speed, impossible

        geo_results = df.apply(calculate_geo_metrics, axis=1)
        df["travel_distance_km"] = [g[0] for g in geo_results]
        df["travel_speed_kmh"] = [g[1] for g in geo_results]
        df["impossible_travel_flag"] = [g[2] for g in geo_results]

        df.drop(columns=["prev_country", "prev_timestamp", "time_delta_hours"], errors="ignore", inplace=True)

        # ── 5. User Behaviour Profiles (Historical Baselines) ─────────
        user_stats = df.groupby("user_id").agg(
            user_avg_login_hour=("hour", "mean"),
            user_avg_session_duration=("session_duration", "mean"),
            user_avg_bytes_transferred=("bytes_transferred", "mean"),
            resource_diversity=("resource", "nunique"),
            unique_ip_count=("ip_address", "nunique"),
        ).reset_index()

        df = df.merge(user_stats, on="user_id", how="left")

        # ── 6. Network Features ───────────────────────────────────────
        df["bytes_transferred"] = df["bytes_transferred"].fillna(0).astype(float)
        df["is_vpn"] = (df["country_changed"] & (df["travel_speed_kmh"] > 1000.0)).astype(int)
        df["is_private_network"] = df["ip_address"].apply(
            lambda ip: 1 if str(ip).startswith(("10.", "192.168.", "172.")) else 0
        )

        # ── 7. Resource Features ──────────────────────────────────────
        df["is_sensitive_resource"] = df["resource"].apply(
            lambda r: 1 if r in SENSITIVE_RESOURCES else 0
        )

        # First time access check per user-resource pair
        df["cum_access"] = df.groupby(["user_id", "resource"]).cumcount() + 1
        df["first_time_access"] = (df["cum_access"] == 1).astype(int)

        # Resource access frequency
        res_freq = df.groupby("resource")["id" if "id" in df.columns else "user_id"].transform("count")
        df["resource_access_frequency"] = res_freq.fillna(1).astype(float)
        df.drop(columns=["cum_access"], errors="ignore", inplace=True)

        # Resource category
        df["resource_category"] = df["resource"].apply(
            lambda r: RESOURCE_CATEGORIES.get(r, "General")
        )

        return df

    def fit_transform(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Fit preprocessors and return scaled feature matrix X and label vector y."""
        df_feat = self.extract_features(df)

        # Numerical features scaling
        X_num = df_feat[NUMERICAL_FEATURE_COLS].fillna(0).values
        X_num_scaled = self.scaler.fit_transform(X_num)

        # Categorical features one-hot encoding
        X_cat = df_feat[CATEGORICAL_FEATURE_COLS].fillna("Unknown").values
        X_cat_encoded = self.onehot_encoder.fit_transform(X_cat)

        # Concatenate numerical and categorical features
        X = np.hstack([X_num_scaled, X_cat_encoded])

        # Target label encoding
        target_col = "attack_type" if "attack_type" in df_feat.columns else "label"
        if target_col in df_feat.columns:
            y = self.label_encoder.fit_transform(df_feat[target_col])
        else:
            y = np.zeros(len(df_feat), dtype=int)

        self.is_fitted = True
        return X, y

    def transform(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Transform raw event DataFrame using fitted preprocessors."""
        if not self.is_fitted:
            raise RuntimeError("FeatureEngineer must be fitted before transform().")

        df_feat = self.extract_features(df)

        X_num = df_feat[NUMERICAL_FEATURE_COLS].fillna(0).values
        X_num_scaled = self.scaler.transform(X_num)

        X_cat = df_feat[CATEGORICAL_FEATURE_COLS].fillna("Unknown").values
        X_cat_encoded = self.onehot_encoder.transform(X_cat)

        X = np.hstack([X_num_scaled, X_cat_encoded])

        target_col = "attack_type" if "attack_type" in df_feat.columns else "label"
        if target_col in df_feat.columns:
            # Handle unseen labels gracefully
            known_labels = set(self.label_encoder.classes_)
            labels = df_feat[target_col].apply(lambda l: l if l in known_labels else "Normal")
            y = self.label_encoder.transform(labels)
        else:
            y = np.zeros(len(df_feat), dtype=int)

        return X, y

    def create_sequence_data(
        self, df: pd.DataFrame, sequence_length: int = 10
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare sequence sequences (user events) for LSTM sequence model."""
        df_sorted = df.sort_values(by=["user_id", "timestamp"]).reset_index(drop=True)

        if not self.action_tokenizer:
            unique_actions = df_sorted["action"].unique().tolist()
            self.action_tokenizer = {act: idx + 1 for idx, act in enumerate(sorted(unique_actions))}

        sequences: list[list[int]] = []
        labels: list[int] = []

        label_map = {cls: idx for idx, cls in enumerate(self.label_encoder.classes_)} if self.is_fitted else {}

        for user_id, group in df_sorted.groupby("user_id"):
            tokens = [self.action_tokenizer.get(a, 0) for a in group["action"]]
            user_labels = group["label"].tolist() if "label" in group.columns else ["Normal"] * len(tokens)

            for i in range(len(tokens) - sequence_length + 1):
                seq = tokens[i : i + sequence_length]
                lbl_str = user_labels[i + sequence_length - 1]
                lbl_idx = label_map.get(lbl_str, 0)

                sequences.append(seq)
                labels.append(lbl_idx)

        if not sequences:
            return np.zeros((0, sequence_length), dtype=int), np.zeros((0,), dtype=int)

        return np.array(sequences, dtype=int), np.array(labels, dtype=int)

    def save(self, model_dir: Path | str) -> None:
        """Save fitted preprocessor pipeline to disk."""
        model_dir = Path(model_dir)
        model_dir.mkdir(parents=True, exist_ok=True)

        state = {
            "scaler": self.scaler,
            "onehot_encoder": self.onehot_encoder,
            "label_encoder": self.label_encoder,
            "action_tokenizer": self.action_tokenizer,
            "is_fitted": self.is_fitted,
        }
        joblib.dump(state, model_dir / "preprocessor.joblib")

    @classmethod
    def load(cls, model_dir: Path | str) -> FeatureEngineer:
        """Load fitted preprocessor pipeline from disk."""
        model_dir = Path(model_dir)
        filepath = model_dir / "preprocessor.joblib"

        if not filepath.exists():
            raise FileNotFoundError(f"Preprocessor file not found at {filepath}")

        state = joblib.load(filepath)
        fe = cls()
        fe.scaler = state["scaler"]
        fe.onehot_encoder = state["onehot_encoder"]
        fe.label_encoder = state["label_encoder"]
        fe.action_tokenizer = state["action_tokenizer"]
        fe.is_fitted = state["is_fitted"]
        return fe
