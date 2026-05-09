from .memory import MemoryManager
from .llm import MockLLM, LLMProvider
from .tools import get_default_tools

class JARVIS:
    def __init__(self, memory_manager: MemoryManager = None, llm_provider: LLMProvider = None, tools: list = None):
        self.memory_manager = memory_manager or MemoryManager()
        self.llm_provider = llm_provider or MockLLM()
        self.tools = tools if tools is not None else get_default_tools()

    def _extract_facts(self, query: str):
        # In a real scenario, we would ask the LLM: "Does this sentence contain a personal fact about the user? If so, extract it."
        # For now, we'll use a simple heuristic or a secondary LLM call if using a real provider.
        if "i love" in query.lower() or "my favorite" in query.lower() or "i live in" in query.lower():
            fact = query.strip()
            self.remember_fact(f"User fact: {fact}")

    def _select_tool(self, query: str):
        # Determine which tool to use.
        # If using a real LLM, we should ask it: "Given these tools: [names], which one is needed for: [query]?"
        # Falling back to keyword matching if LLM is mock or fails.
        for tool in self.tools:
            if any(kw in query.lower() for kw in tool.keywords):
                return tool
        return None

    def ask(self, query: str) -> str:
        # Automatic Fact Extraction
        self._extract_facts(query)

        # Check for tool triggering
        triggered_tool = self._select_tool(query)
        tool_output = triggered_tool.execute(query) if triggered_tool else None

        # Retrieve context from memory
        past_memories = self.memory_manager.get_memories(category="conversation", limit=5)
        personal_facts = self.memory_manager.get_memories(category="fact", limit=10)

        context = []
        if personal_facts:
            context.append("Personal facts about the user:")
            context.extend([f"- {f['content']}" for f in personal_facts])

        context.extend([m['content'] for m in past_memories])  # Last 5 messages for context

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
