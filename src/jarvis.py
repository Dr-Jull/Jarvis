from .memory import MemoryManager
from .llm import MockLLM, LLMProvider
from .tools import get_default_tools

class JARVIS:
    def __init__(self, memory_manager: MemoryManager = None, llm_provider: LLMProvider = None, tools: list = None):
        self.memory_manager = memory_manager or MemoryManager()
        self.llm_provider = llm_provider or MockLLM()
        self.tools = tools if tools is not None else get_default_tools()

    def ask(self, query: str) -> str:
        # Check for tool triggering
        tool_output = None
        triggered_tool = None

        for tool in self.tools:
            if any(kw in query.lower() for kw in tool.keywords):
                triggered_tool = tool
                tool_output = tool.execute(query)
                break

        # Retrieve context from memory
        past_memories = self.memory_manager.get_memories(category="conversation", limit=5)
        context = [m['content'] for m in past_memories]  # Last 5 messages for context

        if tool_output:
            context.append(f"Tool Output ({triggered_tool.name}): {tool_output}")
            query_with_tool = f"Based on this information: {tool_output}, answer the user: {query}"
            response = self.llm_provider.generate_response(query_with_tool, context)
        else:
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
