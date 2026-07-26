import os
import sys
import json
import pandas as pd
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from app.ml.predict import PredictionPipeline

def test_payloads():
    pipeline = PredictionPipeline()
    
    payloads = {
        "Normal": {
            "event_id": "test_normal_001", "user_id": 1, "device_id": 1,
            "timestamp": "2026-10-31T09:00:00Z", "action": "Login",
            "resource": "Email", "status": "Success", "bytes_transferred": 250,
            "ip_address": "192.168.1.10", "location": "USA", "session_duration": 120,
            "failed_attempts": 0, "login_status": "success", "country": "USA",
            "authentication_method": "SSO"
        },
        "BruteForce": {
            "event_id": "test_brute_001", "user_id": 1, "device_id": 1,
            "timestamp": "2026-10-31T08:15:00Z", "action": "Login",
            "resource": "Active Directory", "status": "Success", "bytes_transferred": 500,
            "ip_address": "192.168.1.10", "location": "USA", "session_duration": 1,
            "failed_attempts": 25, "login_status": "success", "country": "USA",
            "authentication_method": "Password"
        }
    }
    
    for name, event in payloads.items():
        print(f"--- {name} ---")
        try:
            # Predict with empty history
            res = pipeline.predict_event(event, [])
            print(f"Prediction: {res['prediction']}")
            print(f"Confidence: {res['confidence']}")
            print(f"B-Score: {res['behavior_score']}, S-Score: {res['sequence_score']}")
            print(f"Top features: {res['top_features']}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_payloads()
