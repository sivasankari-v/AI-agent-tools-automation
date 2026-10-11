"""
Tools Module - Defines all tools available to the AI Agent.
Each tool follows a standard interface: name, description, and execute method.
"""

import re
import math
from datetime import datetime
from typing import Dict, Any

class CalculatorTool:
    """Performs mathematical calculations - demonstrates Function Calling."""
    name = "calculator"
    description = "Use for any mathematical calculations, arithmetic, percentages."

    def execute(self, query: str) -> str:
        try:
            # Sanitize input to allow only math characters
            expression = re.findall(r'[\d\+\-\*/\(\)\.\% ]+', query)
            if not expression:
                return "Error: No valid math expression found."
            
            safe_expr = "".join(expression).strip()
            # Prevent dangerous eval
            if len(safe_expr) > 100:
                return "Error: Expression too long."
            
            result = eval(safe_expr, {"__builtins__": None}, {"math": math})
            return f"Calculation: {safe_expr} = {result}"
        except Exception as e:
            return f"Calculator Error: Unable to calculate. {str(e)}"

class WeatherTool:
    """Simulates external API integration for weather data."""
    name = "weather_api"
    description = "Use to get weather information for a city. Requires city name."

    def execute(self, city: str) -> str:
        # Simulated API response - can be replaced with OpenWeatherMap API
        mock_database = {
            "chennai": {"temp": "32°C", "condition": "Sunny", "humidity": "75%"},
            "salem": {"temp": "30°C", "condition": "Partly Cloudy", "humidity": "65%"},
            "bangalore": {"temp": "26°C", "condition": "Light Rain", "humidity": "80%"},
            "coimbatore": {"temp": "28°C", "condition": "Pleasant", "humidity": "60%"},
            "delhi": {"temp": "38°C", "condition": "Hot", "humidity": "45%"}
        }
        city_key = city.lower().strip()
        data = mock_database.get(city_key, {"temp": "28°C", "condition": "Clear", "humidity": "60%"})
        return f"Weather API Response | City: {city.title()} | Temp: {data['temp']} | Condition: {data['condition']} | Humidity: {data['humidity']}"

class TodoTool:
    """Manages agent state and memory - demonstrates State Management."""
    name = "todo_manager"
    description = "Use to add, list, or manage tasks. Demonstrates agent memory."

    def __init__(self):
        self.tasks = []

    def execute(self, action: str, task: str = "") -> str:
        if "add" in action.lower() or task:
            task_entry = {
                "task": task or action,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "status": "pending"
            }
            self.tasks.append(task_entry)
            return f"Task Added Successfully. Total pending tasks: {len(self.tasks)}. Task: '{task_entry['task']}'"
        else:
            return f"Current Tasks in Memory: {len(self.tasks)} tasks stored."

class EmailTool:
    """Demonstrates automation and content generation."""
    name = "email_drafter"
    description = "Use to draft professional emails for any purpose."

    def execute(self, purpose: str) -> str:
        return f"""Email Draft Generated:

Subject: Regarding {purpose.title()}

Dear Sir/Madam,

I hope this email finds you well.

I am writing to discuss {purpose}. I would appreciate your guidance and support regarding this matter.

Please let me know a suitable time to discuss further.

Thank you for your time and consideration.

Best Regards,
[Your Name]
Automation generated via AI Agent
"""

# Tool Registry
AVAILABLE_TOOLS = {
    "calculator": CalculatorTool(),
    "weather_api": WeatherTool(),
    "todo_manager": TodoTool(),
    "email_drafter": EmailTool()
}