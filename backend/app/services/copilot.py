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
    """Service to handle AI Copilot requests using LangChain Native Tool Binding."""
    
    @staticmethod
    def generate_response(question: str, context: Dict[str, Any]) -> str:
        api_key = os.environ.get("GEMINI_API_KEY")
        
        if api_key and api_key != "paste_your_key_here":
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                from langchain_core.messages import SystemMessage, HumanMessage
                from langchain_core.tools import tool
            except ImportError as e:
                logger.error(f"ImportError in CopilotService: {e}")
                return f"⚠️ **Error:** Failed to import LangChain modules. `{str(e)}`"
                
            try:
                # 1. Define Autonomous Tools (SOAR Actions)
                @tool
                def suspend_user_account(user_id: int, reason: str) -> str:
                    """Suspends a user account in the IAM system (Active Directory/Okta) to prevent further unauthorized access."""
                    logger.info(f"EXECUTING SOAR ACTION: Suspending user {user_id}. Reason: {reason}")
                    time.sleep(1) # Simulated API call
                    return f"✅ **SUCCESS:** User {user_id} has been suspended at the IAM level. Tokens revoked."

                @tool
                def isolate_endpoint(device_id: int) -> str:
                    """Dispatches an EDR signal to network-isolate a compromised endpoint/device."""
                    logger.info(f"EXECUTING SOAR ACTION: Isolating endpoint {device_id}.")
                    time.sleep(1) # Simulated API call
                    return f"✅ **SUCCESS:** Device {device_id} has been network-isolated via CrowdStrike EDR."
                
                tools = [suspend_user_account, isolate_endpoint]
                tools_map = {t.name: t for t in tools}
                
                # 2. Instantiate LLM and Bind Tools directly (Bypasses AgentExecutor)
                llm = ChatGoogleGenerativeAI(
                    model="gemini-2.5-flash-lite",
                    google_api_key=api_key,
                    temperature=0.2
                )
                llm_with_tools = llm.bind_tools(tools)
                
                # 3. Construct the Message History
                system_prompt = (
                    "You are an Autonomous AI Security Analyst inside a Security Operations Center (SOC). "
                    "You are assisting a human analyst. Answer their question based strictly on the provided telemetry context.\n\n"
                    "If the user explicitly asks you to take action (e.g., 'suspend the user', 'isolate the device'), "
                    "you MUST use your available tools to execute that action immediately.\n\n"
                    "Format beautifully with Markdown. Do not make up data outside the context.\n\n"
                    f"--- TELEMETRY CONTEXT ---\n{json.dumps(context, indent=2)}"
                )
                
                messages = [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=question)
                ]
                
                # 4. Invoke LLM
                ai_msg = llm_with_tools.invoke(messages)
                
                # 5. Check if the AI decided to call a tool
                if hasattr(ai_msg, "tool_calls") and ai_msg.tool_calls:
                    responses = []
                    for tool_call in ai_msg.tool_calls:
                        selected_tool = tools_map[tool_call["name"].lower()]
                        # Execute the python function manually
                        tool_msg = selected_tool.invoke(tool_call["args"])
                        responses.append(tool_msg)
                    return "\n\n".join(responses)
                else:
                    # AI didn't use a tool, just return its text response safely
                    content = ai_msg.content
                    if isinstance(content, list):
                        content = " ".join(str(c.get("text", "")) for c in content if isinstance(c, dict))
                    return str(content) if content else "I could not generate a response."
                
            except Exception as e:
                logger.error(f"LangChain Tool Error: {str(e)}")
                return f"⚠️ **LangChain Tool Error:** {str(e)}"
        
        # --- Fast Offline Mock Fallback ---
        return "I am currently running in offline mock mode. Please add a GEMINI_API_KEY to enable Autonomous SOAR capabilities."
