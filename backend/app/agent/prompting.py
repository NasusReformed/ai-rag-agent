import json
from typing import Any


SYSTEM_PROMPT = """You are a production AI agent for a SaaS support system.
Follow these rules:
- If a tool is needed, request it using the tool JSON format
- If not, respond normally using the provided context
- Keep answers concise and accurate
"""


def tool_selection_prompt(user_message: str, context: str, tools: list[dict]) -> str:
    tools_json = json.dumps(tools, ensure_ascii=True, indent=2)
    return (
        f"{SYSTEM_PROMPT}\n\n"
        "You must output JSON only.\n"
        "Choose one of:\n"
        "{\"action\": \"tool\", \"tool_name\": \"...\", \"tool_args\": {...}}\n"
        "{\"action\": \"final\", \"final\": \"...\"}\n\n"
        f"Context:\n{context}\n\n"
        f"User message: {user_message}\n\n"
        f"Tools:\n{tools_json}\n"
    )


def final_response_prompt(
    user_message: str, context: str, tool_result: Any | None
) -> str:
    tool_text = json.dumps(tool_result, ensure_ascii=True) if tool_result else "null"
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"Context:\n{context}\n\n"
        f"User message: {user_message}\n\n"
        f"Tool result: {tool_text}\n\n"
        "Respond to the user."
    )
