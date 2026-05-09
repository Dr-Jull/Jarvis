import datetime
from abc import ABC, abstractmethod

class BaseTool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def keywords(self) -> list:
        pass

    @abstractmethod
    def execute(self, query: str) -> str:
        pass

class TimeCheckTool(BaseTool):
    @property
    def name(self):
        return "TimeCheck"

    @property
    def description(self):
        return "Checks the current time."

    @property
    def keywords(self):
        return ["time", "clock", "what time"]

    def execute(self, query: str):
        now = datetime.datetime.now()
        return f"The current time is {now.strftime('%H:%M:%S')}."

from duckduckgo_search import DDGS

class WebSearchTool(BaseTool):
    @property
    def name(self):
        return "WebSearch"

    @property
    def description(self):
        return "Searches the web for information."

    @property
    def keywords(self):
        return ["search", "google", "find out", "who is", "what is", "current"]

    def execute(self, query: str):
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
                if not results:
                    return "No results found."

                formatted_results = "\n".join([f"- {r['title']}: {r['body']}" for r in results])
                return f"[WebSearch] Results for '{query}':\n{formatted_results}"
        except Exception as e:
            return f"WebSearch failed: {e}"

import requests

class WeatherTool(BaseTool):
    @property
    def name(self):
        return "Weather"

    @property
    def description(self):
        return "Checks the weather."

    @property
    def keywords(self):
        return ["weather", "temperature", "rain", "sunny"]

    def execute(self, query: str):
        try:
            # First, get approximate location via IP
            loc_res = requests.get("https://ipapi.co/json/", timeout=5)
            loc_data = loc_res.json()
            lat = loc_data.get("latitude", 51.5074)  # Default to London
            lon = loc_data.get("longitude", -0.1278)
            city = loc_data.get("city", "London")

            # Then, get weather via Open-Meteo
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            weather_res = requests.get(weather_url, timeout=5)
            weather_data = weather_res.json()
            current = weather_data.get("current_weather", {})
            temp = current.get("temperature", "N/A")
            wind = current.get("windspeed", "N/A")

            return f"[Weather] In {city}, it's currently {temp}°C with a wind speed of {wind} km/h."
        except Exception as e:
            return f"Weather check failed: {e}"

class TaskTool(BaseTool):
    def __init__(self, memory_manager):
        self.memory_manager = memory_manager

    @property
    def name(self):
        return "TaskTool"

    @property
    def description(self):
        return "Manages tasks and reminders."

    @property
    def keywords(self):
        return ["task", "todo", "remind me", "list my tasks"]

    def execute(self, query: str):
        if "list" in query.lower() or "show" in query.lower():
            tasks = self.memory_manager.get_memories(category="task")
            if not tasks:
                return "You have no tasks."
            return "Your tasks:\n" + "\n".join([f"- {t['content']}" for t in tasks])

        # Simple extraction for adding tasks
        task_content = query.replace("remind me to", "").replace("add task", "").strip()
        self.memory_manager.add_memory("task", task_content)
        return f"Task added: {task_content}"

def get_default_tools(memory_manager=None):
    tools = [TimeCheckTool(), WebSearchTool(), WeatherTool()]
    if memory_manager:
        tools.append(TaskTool(memory_manager))
    return tools
