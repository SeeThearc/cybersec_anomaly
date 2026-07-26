import os
import json
import logging
import time
from typing import Dict, Any
from dotenv import load_dotenv

# Force load the .env file so os.environ picks it up!
load_dotenv()

# Try to import either the new or the classic Gemini SDK
HAS_NEW_SDK = False
HAS_CLASSIC_SDK = False

try:
    from google import genai
    HAS_NEW_SDK = True
except ImportError:
    try:
        import google.generativeai as genai_classic
        HAS_CLASSIC_SDK = True
    except ImportError:
        pass

logger = logging.getLogger(__name__)

class CopilotService:
    """Service to handle AI Copilot requests."""
    
    @staticmethod
    def generate_response(question: str, context: Dict[str, Any]) -> str:
        api_key = os.environ.get("GEMINI_API_KEY")
        
        # If we have an API key, ALWAYS try to use real AI
        if api_key and api_key != "paste_your_key_here":
            if not HAS_NEW_SDK and not HAS_CLASSIC_SDK:
                return "⚠️ **Error:** You have an API key, but the SDK is not installed. Please run `pip install google-generativeai` in the backend folder."
                
            prompt = (
                "You are an expert AI Security Analyst inside a Security Operations Center (SOC). "
                "You are assisting a human analyst. Answer their question based strictly on the provided telemetry context. "
                "Keep your response concise, professional, and highly actionable. Format with Markdown. "
                "Do not make up data outside the context.\n\n"
                f"--- TELEMETRY CONTEXT ---\n{json.dumps(context, indent=2)}\n\n"
                f"Analyst Question: {question}"
            )
            
            try:
                if HAS_NEW_SDK:
                    client = genai.Client(api_key=api_key)
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=prompt,
                    )
                    return response.text
                elif HAS_CLASSIC_SDK:
                    genai_classic.configure(api_key=api_key)
                    model = genai_classic.GenerativeModel('gemini-2.5-flash')
                    response = model.generate_content(prompt)
                    return response.text
            except Exception as e:
                logger.error(f"Gemini API Error: {str(e)}")
                return f"⚠️ **Gemini API Error:** {str(e)}"
        
        # --- Fast Offline Mock Fallback (Only runs if no API key is found) ---
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
