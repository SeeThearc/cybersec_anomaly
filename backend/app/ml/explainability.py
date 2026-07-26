"""Explainability Engine for Machine Learning Predictions.

Uses SHAP (SHapley Additive exPlanations) to interpret the XGBoost Attack
Classifier. Translates mathematical feature importance into human-readable,
plain English explanations for the Security Operations Center (SOC).
"""

from __future__ import annotations

from typing import Any, Dict, List

import numpy as np
import shap
from xgboost import XGBClassifier


# Dictionary mapping technical feature names to human-readable explanations
HUMAN_TRANSLATIONS: Dict[str, str] = {
    # Custom ML Scores
    "behavior_score": "User exhibited highly anomalous behavior compared to their historical baseline",
    "sequence_score": "User performed a highly unpredictable sequence of actions",
    
    # Time Features
    "hour": "Action occurred at an unusual hour",
    "is_weekend": "Action occurred during the weekend",
    "is_working_hours": "Action occurred outside normal working hours",
    
    # Auth Features
    "failed_attempts": "Multiple failed login attempts detected",
    "attempts_per_minute": "High frequency of actions performed within a single minute",
    
    # Device Features
    "known_device": "Login occurred from an unrecognized device",
    "device_changed": "User switched to a different device during the session",
    
    # Geo Features
    "country_changed": "User logged in from a different country than their previous session",
    "travel_distance_km": "User logged in from a completely new geographical location",
    "travel_speed_kmh": "User traveled an impossible distance in a short time (Impossible Travel)",
    "impossible_travel_flag": "Physical travel impossibility detected between consecutive logins",
    
    # Network Features
    "is_vpn": "Connection originated from a known VPN or anonymizing proxy",
    "unique_ip_count": "User accessed the system from an unusually high number of different IP addresses",
    
    # Resource Features
    "is_sensitive_resource": "User accessed a highly sensitive critical resource",
    "first_time_access": "User accessed a resource they have never interacted with before",
    "resource_access_frequency": "User accessed a resource with unusual frequency",
    "resource_diversity": "User accessed an unusually broad range of different resources",
    "bytes_transferred": "Unusually large amount of data was transferred",
}


class ExplainabilityEngine:
    """Engine to generate SHAP-based explanations for XGBoost predictions."""

    def __init__(self, model: XGBClassifier, feature_names: List[str]) -> None:
        """
        Initializes the explainer.
        
        Args:
            model: The trained XGBClassifier model.
            feature_names: Ordered list of feature names corresponding to the columns in the training matrix X.
        """
        self.model = model
        self.feature_names = feature_names
        # Create the SHAP TreeExplainer for the XGBoost model
        self.explainer = shap.TreeExplainer(self.model)

    def explain_prediction(
        self, X_instance: np.ndarray, predicted_class_index: int, top_n: int = 4
    ) -> Dict[str, Any]:
        """
        Extracts the top driving features for a specific prediction.
        
        Args:
            X_instance: A single row of features (1D or 2D array of shape (1, n_features)).
            predicted_class_index: The integer index of the predicted class.
            top_n: Number of top reasons to return.
            
        Returns:
            Dictionary containing 'machine_explanation' and 'human_explanation'.
        """
        if X_instance.ndim == 1:
            X_instance = X_instance.reshape(1, -1)

        # Calculate SHAP values for this specific instance
        shap_values = self.explainer.shap_values(X_instance)
        
        # XGBoost multi:softprob returns a list of shap_values, one array per class.
        # We only care about the SHAP values explaining the *predicted* class.
        if isinstance(shap_values, list):
            class_shap_values = shap_values[predicted_class_index][0]
        else:
            # For binary classification or if xgboost outputs a 3D array (num_samples, num_features, num_classes)
            if shap_values.ndim == 3:
                class_shap_values = shap_values[0, :, predicted_class_index]
            else:
                class_shap_values = shap_values[0]

        # Get indices of features sorted by their absolute SHAP contribution (highest first)
        top_indices = np.argsort(np.abs(class_shap_values))[::-1]
        
        machine_explanation = {}
        human_explanation = []
        
        count = 0
        for idx in top_indices:
            if count >= top_n:
                break
                
            feat_val = class_shap_values[idx]
            # Only consider features that positively contributed to predicting THIS specific attack class.
            # (If it's negative, it means this feature pushed the model AWAY from predicting this class).
            if feat_val > 0.0:
                feat_name = self.feature_names[idx]
                machine_explanation[feat_name] = round(float(feat_val), 4)
                
                # Translate to human-readable reason
                human_reason = HUMAN_TRANSLATIONS.get(feat_name, f"Unusual pattern detected in {feat_name}")
                human_explanation.append(f"✓ {human_reason}")
                
                count += 1
                
        # Fallback if no positive features were found (rare, but possible near decision boundaries)
        if not human_explanation:
            human_explanation.append("✓ Combination of subtle behavioral anomalies.")

        return {
            "machine_explanation": machine_explanation,
            "human_explanation": human_explanation,
        }
