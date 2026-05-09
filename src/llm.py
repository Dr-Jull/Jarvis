from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def generate_response(self, prompt: str, context: list = None) -> str:
        pass

class MockLLM(LLMProvider):
    def generate_response(self, prompt: str, context: list = None) -> str:
        if "name" in prompt.lower():
            return "My name is JARVIS. How can I assist you today?"
        if "who are you" in prompt.lower():
            return "I am JARVIS, your secure personal assistant."
        return f"I heard you say: '{prompt}'. As your secure assistant, I'm processing that."

import requests
import json

class OllamaProvider(LLMProvider):
    def __init__(self, model_name="llama3", base_url="http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url

    def generate_response(self, prompt: str, context: list = None) -> str:
        url = f"{self.base_url}/api/generate"

        full_prompt = ""
        if context:
            full_prompt += "Context:\n" + "\n".join(context) + "\n\n"
        full_prompt += f"User: {prompt}\nAssistant:"

        payload = {
            "model": self.model_name,
            "prompt": full_prompt,
            "stream": False
        }

        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json().get("response", "No response from Ollama.")
        except requests.exceptions.ConnectionError:
            return "Connection Error: Could not reach Ollama. Please ensure Ollama is running (e.g., 'ollama serve')."
        except requests.exceptions.Timeout:
            return "Timeout Error: Ollama is taking too long to respond."
        except Exception as e:
            return f"Error communicating with Ollama: {e}"

class LocalLLM(LLMProvider):
    def __init__(self, model_name="llama3"):
        self.model_name = model_name

    def generate_response(self, prompt: str, context: list = None) -> str:
        return f"[Local LLM {self.model_name}] Simulated response to: {prompt}"
