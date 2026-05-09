from .memory import MemoryManager
from .llm import MockLLM, LLMProvider

class JARVIS:
    def __init__(self, memory_manager: MemoryManager = None, llm_provider: LLMProvider = None):
        self.memory_manager = memory_manager or MemoryManager()
        self.llm_provider = llm_provider or MockLLM()

    def ask(self, query: str) -> str:
        # Retrieve context from memory
        past_memories = self.memory_manager.get_memories(category="conversation", limit=5)
        context = [m['content'] for m in past_memories]  # Last 5 messages for context

        # Generate response
        response = self.llm_provider.generate_response(query, context)

        # Save to memory
        self.memory_manager.add_memory("conversation", f"User: {query}")
        self.memory_manager.add_memory("conversation", f"JARVIS: {response}")

        return response

    def remember_fact(self, fact: str):
        self.memory_manager.add_memory("fact", fact)

    def get_facts(self):
        return self.memory_manager.get_memories(category="fact")
