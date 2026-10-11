"""
AI Agent Core - Implements Understand -> Decide -> Act -> Observe -> Respond loop.
This demonstrates difference between simple Chatbot and Autonomous Agent.
"""

from tools import AVAILABLE_TOOLS
import re
from typing import Tuple, Dict

class AIAgent:
    """
    Autonomous AI Agent with Tool Calling, Memory and State Management.
    """
    
    def __init__(self):
        self.memory = []  # Agent memory for multi-step workflows
        self.state = {"tasks_completed": 0, "tools_used": []}

    def understand_task(self, user_input: str) -> Dict:
        """Step 1: Understand user intent and extract entities."""
        intent = "general"
        entities = {}
        user_lower = user_input.lower()

        if any(k in user_lower for k in ["calculate", "math", "+", "*", "/", "percentage", "sum"]):
            intent = "calculation"
        elif "weather" in user_lower or "temperature" in user_lower:
            intent = "weather_query"
            # Extract city name
            cities = ["chennai", "salem", "bangalore", "coimbatore", "delhi", "mumbai"]
            for city in cities:
                if city in user_lower:
                    entities["city"] = city
                    break
            entities["city"] = entities.get("city", "salem")
        elif any(k in user_lower for k in ["todo", "task", "remind", "add task"]):
            intent = "task_management"
            entities["task"] = user_input
        elif "email" in user_lower or "mail" in user_lower:
            intent = "email_automation"
            entities["purpose"] = user_input.replace("email", "").replace("draft", "").strip()

        return {"intent": intent, "entities": entities, "raw_input": user_input}

    def decide_action(self, understanding: Dict) -> Tuple[str, Dict]:
        """Step 2: Decide which tool to use based on understanding."""
        intent = understanding["intent"]
        entities = understanding["entities"]

        if intent == "calculation":
            return "calculator", {"query": understanding["raw_input"]}
        elif intent == "weather_query":
            return "weather_api", {"city": entities.get("city", "salem")}
        elif intent == "task_management":
            return "todo_manager", {"action": "add", "task": entities.get("task", understanding["raw_input"])}
        elif intent == "email_automation":
            return "email_drafter", {"purpose": entities.get("purpose", "general inquiry")}
        else:
            return "none", {}

    def execute_tool(self, tool_name: str, params: Dict) -> str:
        """Step 3: Execute selected tool."""
        if tool_name == "none":
            return None
        
        tool = AVAILABLE_TOOLS.get(tool_name)
        if not tool:
            return f"Error: Tool {tool_name} not found."

        try:
            if tool_name == "calculator":
                result = tool.execute(params.get("query", ""))
            elif tool_name == "weather_api":
                result = tool.execute(params.get("city", ""))
            elif tool_name == "todo_manager":
                result = tool.execute(params.get("action", ""), params.get("task", ""))
            elif tool_name == "email_drafter":
                result = tool.execute(params.get("purpose", ""))
            else:
                result = "Tool executed."

            # Update state
            self.state["tasks_completed"] += 1
            self.state["tools_used"].append(tool_name)
            self.memory.append({"tool": tool_name, "result": result})
            
            return result
        except Exception as e:
            return f"Tool Execution Failed: {str(e)}"

    def generate_response(self, understanding: Dict, tool_result: str) -> str:
        """Step 4 & 5: Process result and respond."""
        if tool_result is None:
            return """
I am an AI Agent with tool-calling capabilities. Unlike a simple chatbot that only generates text, I can:

**My Capabilities:**
- 🧮 **Calculator Tool:** `calculate 45*12` or `what is 20% of 500`
- 🌦️ **Weather Tool (API Integration):** `weather in Chennai`
- ✅ **ToDo Tool (State & Memory):** `add todo complete Module 5`
- 📧 **Email Tool (Automation):** `draft email for internship application`

**Agent Architecture:** Understand Task → Decide Action → Use Tool → Process Result → Respond

Try asking me to use any of these tools!
"""
        
        return f"""
**Agent Execution Trace:**

1. **Understand:** Intent=`{understanding['intent']}`, Entities=`{understanding['entities']}`
2. **Decide:** Selected tool based on intent
3. **Act:** Executed tool successfully
4. **Observe:** Received tool output
5. **Respond:** Final answer below

---

{tool_result}

---
*Agent State: {self.state['tasks_completed']} tasks completed | Memory: {len(self.memory)} interactions*
"""