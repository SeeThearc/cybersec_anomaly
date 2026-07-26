import os
import json
import logging
import time
from typing import Dict, Any

try:
    from google import genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

logger = logging.getLogger(__name__)

class CopilotService:
    """Service to handle AI Copilot requests."""
    
    @staticmethod
    def generate_response(question: str, context: Dict[str, Any]) -> str:
        """
        Generate a natural language explanation for an alert or user profile.
        Uses Gemini if the GEMINI_API_KEY environment variable is set and the SDK is installed.
        Otherwise, falls back to a fast deterministic mock.
        """
        api_key = os.environ.get("GEMINI_API_KEY")
        
        # Try real Gemini if available
        if HAS_GENAI and api_key:
            try:
                client = genai.Client(api_key=api_key)
                
                prompt = (
                    "You are an expert AI Security Analyst inside a Security Operations Center (SOC). "
                    "You are assisting a human analyst. Answer their question based strictly on the provided telemetry context. "
                    "Keep your response concise, professional, and highly actionable. Format with Markdown. "
                    "Do not make up data outside the context.\n\n"
                    f"--- TELEMETRY CONTEXT ---\n{json.dumps(context, indent=2)}\n\n"
                    f"Analyst Question: {question}"
                )
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                
                if response.text:
                    return response.text
            except Exception as e:
                logger.error(f"Gemini API Error: {str(e)}. Falling back to mock.")
        
        # --- Fast Offline Mock Fallback ---
        time.sleep(0.1) # Simulate network latency
        question_lower = question.lower()
        
        if "why" in question_lower or "explain" in question_lower or "flagged" in question_lower:
            if "prediction" in context:
                pred = context.get("prediction", "Unknown")
                risk = context.get("risk_level", "Unknown")
                features = context.get("top_features", [])
                feat_str = ", ".join(features) if features else "various anomalies"
                
                return (
                    f"This event was flagged as **{pred}** with a **{risk}** risk level because "
                    f"the ML pipeline detected significant deviations in the following areas: {feat_str}. "
                    f"The sequence of actions strongly matches known {pred} attack signatures."
                )
            
            if "user_details" in context:
                name = context.get("user_details", {}).get("name", "The user")
                return (
                    f"{name} was flagged due to multiple high-risk alerts in their recent history. "
                    "Their behavior profile deviated significantly from their department baseline, "
                    "triggering the Isolation Forest anomaly detector."
                )
                
        if "recommend" in question_lower or "action" in question_lower or "what should i do" in question_lower:
            return (
                "Based on the threat intelligence, I recommend immediately:\n"
                "1. Forcing a password reset.\n"
                "2. Revoking active session tokens.\n"
                "3. Enforcing MFA on the next login attempt."
            )
            
        if "summarize" in question_lower or "trend" in question_lower:
            return (
                "Looking at the recent data, there has been a noticeable uptick in Credential Stuffing "
                "attempts originating from foreign IPs. I recommend tightening the geo-fencing rules "
                "on your authentication endpoints."
            )
            
        return (
            "I've analyzed the telemetry and security events. The patterns indicate anomalous behavior "
            "that deviates from the established baselines. Please review the timeline and top features "
            "for more granular insights."
        )
