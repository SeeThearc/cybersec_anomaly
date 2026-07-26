import os
import json
import logging
import time
from typing import Dict, Any
from dotenv import load_dotenv

# Force load the .env file so os.environ picks it up!
load_dotenv()

logger = logging.getLogger(__name__)

class CopilotService:
    """Service to handle AI Copilot requests using LangChain."""
    
    @staticmethod
    def generate_response(question: str, context: Dict[str, Any]) -> str:
        api_key = os.environ.get("GEMINI_API_KEY")
        
        # If we have an API key, use LangChain LCEL pipeline
        if api_key and api_key != "paste_your_key_here":
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                from langchain_core.prompts import PromptTemplate
                from langchain_core.output_parsers import StrOutputParser
            except ImportError:
                return "⚠️ **Error:** You have an API key, but LangChain is not installed. Please run `pip install -r requirements.txt` in the backend folder."
                
            try:
                # 1. Instantiate the LLM
                llm = ChatGoogleGenerativeAI(
                    model="gemini-3.5-flash",
                    google_api_key=api_key,
                    temperature=0.3
                )
                
                # 2. Define the Prompt Template
                template = """
You are an AI Security Analyst inside a Security Operations Center (SOC). 
You are assisting a human analyst. Answer their question based strictly on the provided telemetry context. 
Provide a crisp, direct, and conversational answer. Summarize the core issue (who, what, and why it was flagged) 
in a few sentences. Do not generate a massive report. 
End by briefly suggesting that the user can ask for a deeper anomaly breakdown or mitigation steps if they need more details.

Format beautifully with Markdown. Do not make up data outside the context.

--- TELEMETRY CONTEXT ---
{telemetry_context}

Analyst Question: {question}
"""
                
                prompt = PromptTemplate(
                    template=template,
                    input_variables=["telemetry_context", "question"]
                )
                
                # 3. Output Parser
                parser = StrOutputParser()
                
                # 4. Construct LCEL Chain
                chain = prompt | llm | parser
                
                # 5. Invoke the chain
                response = chain.invoke({
                    "telemetry_context": json.dumps(context, indent=2),
                    "question": question
                })
                
                return response
                
            except Exception as e:
                logger.error(f"LangChain Gemini Error: {str(e)}")
                return f"⚠️ **LangChain Gemini Error:** {str(e)}"
        
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
