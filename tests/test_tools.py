import unittest
from src.tools import TimeCheckTool, WebSearchTool, WeatherTool

class TestTools(unittest.TestCase):
    def test_time_tool(self):
        tool = TimeCheckTool()
        result = tool.execute("what time is it?")
        self.assertIn("The current time is", result)

    def test_search_tool(self):
        tool = WebSearchTool()
        result = tool.execute("search for Iron Man")
        self.assertIn("[WebSearch]", result)
        self.assertIn("Iron Man", result)

    def test_weather_tool(self):
        tool = WeatherTool()
        result = tool.execute("what's the weather?")
        self.assertIn("[Weather]", result)
        self.assertIn("22°C", result)

if __name__ == "__main__":
    unittest.main()
