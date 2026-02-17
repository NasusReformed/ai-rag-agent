from typing import Any

from app.agent.llm import LLMClient
from app.agent.memory import add_message, ensure_session, get_recent_messages
from app.agent.prompting import final_response_prompt, tool_selection_prompt
from app.api.schemas import AgentRequest
from app.embeddings.encoder import get_encoder
from app.rag.retriever import Retriever
from app.tools.registry import get_tool_registry
from app.utils.json_utils import extract_json
from app.utils.text import format_context


class AgentService:
    def __init__(self) -> None:
        self.llm = LLMClient()
        self.encoder = get_encoder()
        self.retriever = Retriever(self.encoder)
        self.registry = get_tool_registry()

    def chat(self, request: AgentRequest) -> dict:
        session_id = ensure_session(request.session_id, request.user_id)
        add_message(session_id, "user", request.message)

        sources = self.retriever.search(request.message)
        memory = get_recent_messages(session_id)
        context = format_context(sources, memory)

        # For demo: simplified agent logic (skip LLM planning to avoid HF queue issues)
        # In production, use Claude API or Ollama local
        tool_result: Any | None = None
        if "ticket" in request.message.lower() or "crear" in request.message.lower():
            tool_result = self.registry.execute("create_ticket", {
                "title": request.message[:100],
                "priority": "medium",
                "user_id": request.user_id,
                "context": {"source": "chat"}
            })

        # Build answer from context
        answer = f"Based on the knowledge base:\n"
        for src in sources[:2]:
            answer += f"- {src['content'][:100]}...\n"
        if tool_result:
            answer += f"\nTicket created: {tool_result.get('ticket', {}).get('id', 'N/A')}"
        else:
            answer += "\nNo specific action taken. Information retrieved from knowledge base."

        add_message(session_id, "assistant", answer)

        return {
            "session_id": str(session_id),
            "answer": answer,
            "sources": sources,
        }
