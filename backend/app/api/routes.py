from fastapi import APIRouter, HTTPException, Query

from app.agent.agent import AgentService
from app.api.schemas import (
    AgentRequest,
    AgentResponse,
    IndexRequest,
    SearchResponse,
    ToolExecuteRequest,
    ToolExecuteResponse,
    WebhookRequest,
)
from app.core.config import get_settings
from app.core.db import db_execute
from app.embeddings.encoder import get_encoder
from app.rag.retriever import Retriever
from app.tools.registry import get_tool_registry


router = APIRouter(prefix="/api")
settings = get_settings()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/embeddings/index")
def index_documents(request: IndexRequest) -> dict:
    encoder = get_encoder()
    retriever = Retriever(encoder)
    count = retriever.index_documents(request.documents)
    return {"indexed": count}


@router.get("/demo/seed-data")
def get_demo_data() -> dict:
    """Return sample documents for demo purposes."""
    return {
        "documents": [
            {
                "content": "Technical support hours are Monday to Friday from 8 AM to 6 PM EST. For urgent issues outside business hours, please email support@acme.com with subject URGENT.",
                "metadata": {"source": "demo", "category": "support"}
            },
            {
                "content": "Return policy: Items can be returned within 30 days of purchase with original receipt. Refunds are processed within 5-7 business days after inspection.",
                "metadata": {"source": "demo", "category": "policies"}
            },
            {
                "content": "Our pricing plans: Starter ($29/month), Professional ($99/month), Enterprise (custom). All plans include 24/7 API access.",
                "metadata": {"source": "demo", "category": "pricing"}
            },
            {
                "content": "Payment methods accepted: Credit card, PayPal, Wire transfer. Invoices are generated monthly and sent to registered email.",
                "metadata": {"source": "demo", "category": "billing"}
            },
            {
                "content": "SLA guarantees 99.9% uptime for Enterprise customers. For Standard tier, we guarantee 99.5% uptime. Compensation applies if SLA is breached.",
                "metadata": {"source": "demo", "category": "sla"}
            }
        ]
    }


@router.get("/embeddings/search", response_model=list[SearchResponse])
def search_documents(query: str = Query(...), top_k: int = Query(4)) -> list[SearchResponse]:
    encoder = get_encoder()
    retriever = Retriever(encoder)
    return retriever.search(query, top_k=top_k)


@router.post("/agent/chat", response_model=AgentResponse)
def agent_chat(request: AgentRequest) -> AgentResponse:
    agent = AgentService()
    result = agent.chat(request)
    return AgentResponse(**result)


@router.post("/tools/execute", response_model=ToolExecuteResponse)
def execute_tool(request: ToolExecuteRequest) -> ToolExecuteResponse:
    registry = get_tool_registry()
    try:
        result = registry.execute(request.tool_name, request.tool_args)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return ToolExecuteResponse(result=result)


@router.post("/automation/n8n/webhook")
def n8n_webhook(request: WebhookRequest) -> dict:
    db_execute(
        "insert into events (event_type, payload) values (%s, %s)",
        (request.event_type, request.payload),
    )
    return {"status": "received"}
