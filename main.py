import sys
import os
from src.jarvis import JARVIS
from src.memory import MemoryManager
from src.security import SecurityManager
from src.llm import MockLLM, OllamaProvider
from src.voice import VoiceInterface

def main():
    print("--- JARVIS: Secure Personal Assistant ---")

    # Configuration
    llm_type = os.getenv("JARVIS_LLM_TYPE", "mock")
    model_name = os.getenv("JARVIS_MODEL", "llama3")
    voice_enabled = os.getenv("JARVIS_VOICE", "false").lower() == "true"

    print(f"Initializing security and memory systems...")
    security = SecurityManager()
    memory = MemoryManager(security_manager=security)

    if llm_type == "ollama":
        print(f"Connecting to Ollama model: {model_name}...")
        llm = OllamaProvider(model_name=model_name)
    else:
        print("Using Mock LLM...")
        llm = MockLLM()

    voice = VoiceInterface(enabled=voice_enabled)
    jarvis = JARVIS(memory_manager=memory, llm_provider=llm)

    print("JARVIS is online. Type 'exit' to quit.")

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                break

            if not user_input and voice_enabled:
                user_input = voice.listen_for_speech()

            if not user_input:
                continue

            response = jarvis.ask(user_input)
            print(f"JARVIS: {response}")

            if voice_enabled:
                voice.speak_text(response)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred: {e}")

    print("JARVIS going offline. Goodbye.")

if __name__ == "__main__":
    main()
