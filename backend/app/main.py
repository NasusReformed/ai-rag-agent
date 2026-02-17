from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as api_router
from app.core.config import get_settings
from app.core.db import close_pool, init_pool


settings = get_settings()
app = FastAPI(title="AI Agent RAG API", version="1.0.0")


@app.on_event("startup")
def on_startup() -> None:
    init_pool(settings.supabase_db_url)


@app.on_event("shutdown")
def on_shutdown() -> None:
    close_pool()


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

# Serve static files
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def root() -> FileResponse:
    return FileResponse(static_dir / "index.html")
