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

class LocalLLM(LLMProvider):
    def __init__(self, model_name="llama3"):
        self.model_name = model_name

    def generate_response(self, prompt: str, context: list = None) -> str:
        # Skeleton for local LLM invocation (e.g., using Ollama or similar local setup)
        # In a real scenario, this would use subprocess to call the local model.
        return f"[Local LLM {self.model_name}] Simulated response to: {prompt}"
