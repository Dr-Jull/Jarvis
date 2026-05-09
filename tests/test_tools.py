import unittest
from src.tools import TimeCheckTool, WebSearchTool, WeatherTool

class TestTools(unittest.TestCase):
    def test_time_tool(self):
        tool = TimeCheckTool()
        result = tool.execute("what time is it?")
        self.assertIn("The current time is", result)

    def test_search_tool(self):
        tool = WebSearchTool()
        result = tool.execute("python programming")
        # Just check that it returns a string and doesn't crash
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)

    def test_weather_tool(self):
        tool = WeatherTool()
        result = tool.execute("what's the weather?")
        self.assertIn("[Weather]", result)
        # Check that it attempted to get a city and temperature
        self.assertTrue("In" in result)

if __name__ == "__main__":
    unittest.main()
