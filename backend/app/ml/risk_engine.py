"""Risk Scoring Engine.

Aggregates intelligence from Behavior, Sequence, and Classification models
to compute a comprehensive 0-100 Risk Score. Classifies the event into a
Risk Level and provides recommended security actions.
"""

from __future__ import annotations

from typing import Any, Dict, List


def calculate_risk_score(
    behavior_score: float,
    sequence_score: float,
    attack_probability: float,
    historical_risk: float = 0.0,
    is_critical_resource: bool = False,
) -> float:
    """Calculates the weighted risk score (0-100)."""
    # Base weights according to ML pipeline spec
    base_score = (
        (0.35 * behavior_score) +
        (0.25 * sequence_score) +
        (0.25 * attack_probability * 100.0) +
        (0.15 * historical_risk)
    )

    # Boost score slightly if a critical resource is targeted during a risky event
    if is_critical_resource and base_score > 40:
        base_score += 10.0

    return min(max(base_score, 0.0), 100.0)


def get_risk_level(risk_score: float) -> str:
    """Classifies a numeric risk score into a severity level."""
    if risk_score <= 30.0:
        return "LOW"
    elif risk_score <= 60.0:
        return "MEDIUM"
    elif risk_score <= 80.0:
        return "HIGH"
    else:
        return "CRITICAL"


def get_recommended_actions(risk_level: str, attack_type: str) -> List[str]:
    """Generates playbook recommendations based on risk and attack type."""
    actions = []

    if risk_level == "LOW":
        actions.append("Log event for historical baseline.")
    elif risk_level == "MEDIUM":
        actions.append("Flag event for review.")
        actions.append("Monitor subsequent user actions for 24 hours.")
    elif risk_level == "HIGH":
        actions.append("Send alert to Security Operations Center (SOC).")
        actions.append("Require Multi-Factor Authentication (MFA) for next login.")
    elif risk_level == "CRITICAL":
        actions.append("IMMEDIATE: Block IP Address.")
        actions.append("IMMEDIATE: Suspend User Account.")
        actions.append("Page incident response team.")

    if attack_type == "BruteForce":
        actions.append("Implement rate limiting on authentication endpoints.")
    elif attack_type == "LateralMovement":
        actions.append("Isolate compromised endpoint from network.")
    elif attack_type == "LowSlowExfiltration":
        actions.append("Throttle outbound data transfers.")
    elif attack_type == "CredentialStuffing":
        actions.append("Force password reset on affected account.")

    return actions


def evaluate_event(
    behavior_score: float,
    sequence_score: float,
    attack_type: str,
    attack_confidence: float,
    historical_risk: float = 0.0,
    is_critical_resource: bool = False,
) -> Dict[str, Any]:
    """Main entrypoint to evaluate an event and generate the final risk profile."""
    # If the classifier predicts Normal, the attack probability is effectively 0 for risk scoring purposes.
    attack_prob = 0.0 if attack_type == "Normal" else attack_confidence

    score = calculate_risk_score(
        behavior_score=behavior_score,
        sequence_score=sequence_score,
        attack_probability=attack_prob,
        historical_risk=historical_risk,
        is_critical_resource=is_critical_resource,
    )

    level = get_risk_level(score)
    actions = get_recommended_actions(level, attack_type)

    return {
        "risk_score": round(score, 2),
        "risk_level": level,
        "attack_type": attack_type,
        "attack_confidence": round(attack_confidence, 4),
        "recommended_actions": actions,
    }
