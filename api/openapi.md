# API Notes

All endpoints are under `/api`.

- `POST /api/agent/chat` : Agent chat (RAG + tool calling)
- `POST /api/embeddings/index` : Index documents
- `GET /api/embeddings/search` : Semantic search
- `POST /api/tools/execute` : Execute a tool directly
- `POST /api/automation/n8n/webhook` : n8n webhook integration
- `GET /api/health` : Health check
