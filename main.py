import sys
from src.jarvis import JARVIS
from src.memory import MemoryManager
from src.security import SecurityManager
from src.llm import MockLLM

def main():
    print("--- JARVIS: Secure Personal Assistant ---")
    print("Initializing security and memory systems...")

    security = SecurityManager()
    memory = MemoryManager(security_manager=security)
    jarvis = JARVIS(memory_manager=memory, llm_provider=MockLLM())

    print("JARVIS is online. Type 'exit' to quit.")

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                break

            response = jarvis.ask(user_input)
            print(f"JARVIS: {response}")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"An error occurred: {e}")

    print("JARVIS going offline. Goodbye.")

if __name__ == "__main__":
    main()
