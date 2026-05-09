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

class WebSearchTool(BaseTool):
    @property
    def name(self):
        return "WebSearch"

    @property
    def description(self):
        return "Searches the web for information."

    @property
    def keywords(self):
        return ["search", "google", "find out", "who is", "what is"]

    def execute(self, query: str):
        # Simulated search result
        return f"[WebSearch] I found some information about '{query}'. (Simulated search results)"

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
        # Simulated weather result
        return f"[Weather] The weather is currently clear and 22°C. (Simulated data)"

def get_default_tools():
    return [TimeCheckTool(), WebSearchTool(), WeatherTool()]
