from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class DocumentInput(BaseModel):
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class IndexRequest(BaseModel):
    documents: List[DocumentInput]


class SearchResponse(BaseModel):
    id: str
    content: str
    metadata: Dict[str, Any]
    score: float
    
    class Config:
        from_attributes = True


class AgentRequest(BaseModel):
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    message: str


class AgentResponse(BaseModel):
    session_id: str
    answer: str
    sources: List[SearchResponse]


class ToolExecuteRequest(BaseModel):
    tool_name: str
    tool_args: Dict[str, Any] = Field(default_factory=dict)


class ToolExecuteResponse(BaseModel):
    result: Dict[str, Any]


class WebhookRequest(BaseModel):
    event_type: str
    payload: Dict[str, Any] = Field(default_factory=dict)
