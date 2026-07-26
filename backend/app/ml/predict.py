import json
import logging
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
import numpy as np

# ML Pipeline Modules
from app.ml.feature_engineering import FeatureEngineer, NUMERICAL_FEATURE_COLS, CATEGORICAL_FEATURE_COLS
from app.ml.behavior_model import BehaviorProfiler
from app.ml.sequence_model import SequenceProfiler
from app.ml.classifier import AttackClassifier
from app.ml.risk_engine import calculate_risk_score, get_risk_level, get_recommended_actions
from app.ml.explainability import ExplainabilityEngine

# ── Configuration ────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODELS_DIR = BASE_DIR / "trained_models"

logger = logging.getLogger(__name__)


# ── Prediction Pipeline ──────────────────────────────────────────────────────

class PredictionPipeline:
    """End-to-End UEBA Prediction Pipeline for real-time inference."""

    def __init__(self, models_dir: Path | str = MODELS_DIR) -> None:
        self.models_dir = Path(models_dir)
        self.is_loaded = False
        
        self.fe = None
        self.behavior_profiler = None
        self.sequence_profiler = None
        self.classifier = None
        self.explainer = None
        self.feature_names = []
        
        # We eagerly load models so the API responds instantly
        self.load_models()

    def load_models(self) -> None:
        """Load all trained ML models from disk."""
        logger.info(f"Loading UEBA models from {self.models_dir}...")
        
        try:
            # 1. Feature Engineer
            self.fe = FeatureEngineer.load(self.models_dir)
            
            # 2. Behavior Profiler (Isolation Forest + Autoencoder)
            self.behavior_profiler = BehaviorProfiler.load(self.models_dir)
            
            # 3. Sequence Profiler (LSTM)
            self.sequence_profiler = SequenceProfiler.load(self.models_dir)
            
            # 4. Attack Classifier (XGBoost)
            self.classifier = AttackClassifier.load(self.models_dir)
            
            # Setup feature names for SHAP
            self.feature_names = NUMERICAL_FEATURE_COLS.copy()
            self.feature_names.extend(
                self.fe.onehot_encoder.get_feature_names_out(CATEGORICAL_FEATURE_COLS)
            )
            self.feature_names.extend(["behavior_score", "sequence_score"])

            # 5. Explainability Engine (SHAP)
            self.explainer = ExplainabilityEngine(self.classifier.model, self.feature_names)
            
            self.is_loaded = True
            logger.info("All models loaded successfully.")
            
        except Exception as e:
            logger.error(f"Failed to load ML pipeline models: {str(e)}")
            raise RuntimeError(f"Prediction Pipeline failed to initialize: {str(e)}")

    def predict_event(self, event: Dict[str, Any], user_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Run a single event through the entire UEBA ML cascade.
        
        Args:
            event: A dictionary representing the current event.
            user_history: A list of dictionaries representing the user's last 9 events.
                          If less than 9, padding will be handled automatically.
                          
        Returns:
            JSON-serializable dictionary with the prediction, scores, and explanation.
        """
        if not self.is_loaded:
            raise RuntimeError("Pipeline not loaded. Call load_models() first.")
            
        # 1. Prepare Event Dataframe
        df_event = pd.DataFrame([event])
        
        # 2. Extract Base Features
        X_event, _ = self.fe.transform(df_event)
        
        # 3. Compute Behavior Score
        b_score = self.behavior_profiler.predict_behavior_score(X_event)
        
        # 4. Compute Sequence Score
        # Build the historical sequence for this user ending with this event
        history_df = pd.DataFrame(user_history)
        if len(history_df) > 0:
            df_seq = pd.concat([history_df, df_event], ignore_index=True)
        else:
            df_seq = df_event
            
        # We need a fixed length sequence of length 10
        seq_length = 10
        # Create sequence logic similar to train.py but for a single user
        tokens = [self.fe.action_tokenizer.get(a, 0) for a in df_seq["action"]]
        
        # Pad with 0s if we don't have enough history
        if len(tokens) < seq_length:
            pad = [0] * (seq_length - len(tokens))
            tokens = pad + tokens
            
        # Keep only the last seq_length tokens
        tokens = tokens[-seq_length:]
        X_seq = np.array([tokens], dtype=int)
        
        # Get sequence score
        s_score = self.sequence_profiler.predict_sequence_score(X_seq)
        
        # 5. Attack Classification
        X_combined = self.classifier._prepare_features(X_event, b_score, s_score)
        
        predicted_class_idx = self.classifier.model.predict(X_combined)[0]
        
        # XGBoost outputs integer classes, so we decode it back to the string label
        prediction = self.fe.label_encoder.inverse_transform([predicted_class_idx])[0]
        
        probabilities = self.classifier.model.predict_proba(X_combined)[0]
        confidence = float(probabilities[predicted_class_idx])
        
        # 6. Risk Engine
        # The Risk Engine computes a final 0-100 score based on ML outputs
        historical_risk = 0.0 # Could be fetched from user profile in DB
        critical_resource = event.get("resource") in ["Payroll", "Admin Console", "Database", "Security Console"]
        
        risk_score = calculate_risk_score(
            behavior_score=float(b_score[0]),
            sequence_score=float(s_score[0]),
            attack_probability=float(confidence) if prediction != "Normal" else 0.0,
            historical_risk=historical_risk,
            is_critical_resource=critical_resource
        )
        risk_level = get_risk_level(risk_score)
        actions = get_recommended_actions(risk_level, str(prediction))
        
        # 7. Explainability
        # Only explain if it's an attack or high risk
        if prediction != "Normal" or risk_level in ["HIGH", "CRITICAL"]:
            # Note: We pass the target class index to explain WHY it picked this attack
            explain_result = self.explainer.explain_prediction(
                X_instance=X_combined[0],
                predicted_class_index=predicted_class_idx
            )
            top_features = list(explain_result.get("machine_explanation", {}).keys())
            explanation = " ".join(explain_result.get("human_explanation", []))
        else:
            top_features = []
            explanation = "User behavior is normal and matches historical baseline."

        # 8. Construct Final JSON Response
        response = {
            "prediction": str(prediction),
            "confidence": round(confidence, 4),
            "behavior_score": round(float(b_score[0]), 2),
            "sequence_score": round(float(s_score[0]), 2),
            "risk_score": round(risk_score, 2),
            "risk_level": risk_level,
            "recommended_actions": actions,
            "top_features": top_features,
            "explanation": explanation
        }
        
        return response


# ── Testing ──────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Configure logging for test output
    logging.basicConfig(level=logging.INFO)
    
    # 1. Initialize Pipeline
    print("🚀 Initializing Prediction Pipeline...")
    pipeline = PredictionPipeline()
    
    # 2. Load a dummy event from test.csv
    print("\n📝 Loading sample event from test dataset...")
    test_path = BASE_DIR / "data" / "test.csv"
    if test_path.exists():
        df_test = pd.read_csv(test_path)
        
        # Grab a random event (let's try to find an anomaly if one exists)
        if "attack_type" in df_test.columns:
            attacks = df_test[df_test["attack_type"] != "Normal"]
            if len(attacks) > 0:
                sample = attacks.iloc[0].to_dict()
                print(f"  Selected an actual attack event: {sample['attack_type']}")
            else:
                sample = df_test.iloc[-1].to_dict()
                print("  Selected a normal event (no attacks found in test.csv).")
        else:
            sample = df_test.iloc[-1].to_dict()
            
        # Get history for this user
        user_id = sample.get("user_id")
        user_history = df_test[df_test["user_id"] == user_id].iloc[:-1].tail(9).to_dict(orient="records")
        
        # 3. Predict
        print("\n🔍 Running Inference Pipeline...")
        result = pipeline.predict_event(sample, user_history)
        
        print("\n✅ Prediction JSON Response:")
        print(json.dumps(result, indent=2))
    else:
        print("❌ Cannot test: test.csv not found.")
