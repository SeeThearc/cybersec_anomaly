"""Test script for Risk Scoring Engine verification."""

import json
from app.ml.risk_engine import evaluate_event


def test_risk_scoring() -> None:
    print("Testing Risk Scoring Engine...\n")

    # Scenario 1: Completely normal user
    print("--- Scenario 1: Normal User ---")
    result_normal = evaluate_event(
        behavior_score=5.0,
        sequence_score=10.0,
        attack_type="Normal",
        attack_confidence=0.98,
        historical_risk=0.0,
        is_critical_resource=False,
    )
    print(json.dumps(result_normal, indent=2))
    assert result_normal["risk_level"] == "LOW"

    # Scenario 2: Suspicious behavior but no confirmed attack
    print("\n--- Scenario 2: Suspicious (Medium Risk) ---")
    result_suspicious = evaluate_event(
        behavior_score=65.0,
        sequence_score=50.0,
        attack_type="Normal",
        attack_confidence=0.55,
        historical_risk=10.0,
        is_critical_resource=False,
    )
    print(json.dumps(result_suspicious, indent=2))
    assert result_suspicious["risk_level"] == "MEDIUM"

    # Scenario 3: Brute Force Attack
    print("\n--- Scenario 3: Brute Force (High Risk) ---")
    result_bruteforce = evaluate_event(
        behavior_score=85.0,
        sequence_score=75.0,
        attack_type="BruteForce",
        attack_confidence=0.88,
        historical_risk=20.0,
        is_critical_resource=False,
    )
    print(json.dumps(result_bruteforce, indent=2))
    assert result_bruteforce["risk_level"] == "HIGH"
    assert any("rate limiting" in action for action in result_bruteforce["recommended_actions"])

    # Scenario 4: Lateral Movement to a Critical Resource
    print("\n--- Scenario 4: Lateral Movement (Critical Risk) ---")
    result_lateral = evaluate_event(
        behavior_score=95.0,
        sequence_score=90.0,
        attack_type="LateralMovement",
        attack_confidence=0.95,
        historical_risk=50.0,
        is_critical_resource=True,
    )
    print(json.dumps(result_lateral, indent=2))
    assert result_lateral["risk_level"] == "CRITICAL"
    assert any("Block IP" in action for action in result_lateral["recommended_actions"])

    print("\nAll Risk Scoring Engine tests passed successfully! ✅")


if __name__ == "__main__":
    test_risk_scoring()
