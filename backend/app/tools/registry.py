from dataclasses import dataclass
from typing import Any, Callable, Dict, List

from app.tools.db_tools import get_user, save_document, search_documents
from app.tools.business import create_ticket, log_event


@dataclass
class Tool:
    name: str
    description: str
    args_schema: Dict[str, Any]
    handler: Callable[[Dict[str, Any]], Dict[str, Any]]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def list_for_prompt(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "args_schema": tool.args_schema,
            }
            for tool in self._tools.values()
        ]

    def execute(self, name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        if name not in self._tools:
            raise ValueError(f"Unknown tool: {name}")
        return self._tools[name].handler(args)


def build_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(
        Tool(
            name="save_document",
            description="Save a document to the knowledge base",
            args_schema={"content": "string", "metadata": "object"},
            handler=save_document,
        )
    )
    registry.register(
        Tool(
            name="search_documents",
            description="Search the knowledge base using a query",
            args_schema={"query": "string", "top_k": "number"},
            handler=search_documents,
        )
    )
    registry.register(
        Tool(
            name="get_user",
            description="Fetch a user by id",
            args_schema={"user_id": "string"},
            handler=get_user,
        )
    )
    registry.register(
        Tool(
            name="log_event",
            description="Log a business event",
            args_schema={"event_type": "string", "payload": "object"},
            handler=log_event,
        )
    )
    registry.register(
        Tool(
            name="create_ticket",
            description="Create a support ticket",
            args_schema={"title": "string", "priority": "string", "user_id": "string", "context": "object"},
            handler=create_ticket,
        )
    )
    return registry


def get_tool_registry() -> ToolRegistry:
    return build_registry()
