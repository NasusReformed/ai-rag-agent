from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = Field(..., alias="DATABASE_URL")

    llm_provider: str = Field("hf", alias="LLM_PROVIDER")
    hf_api_token: str = Field("", alias="HF_API_TOKEN")
    hf_model: str = Field("meta-llama/Llama-3.2-3B-Instruct", alias="HF_MODEL")
    ollama_base_url: str = Field("http://localhost:11434", alias="OLLAMA_BASE_URL")
    ollama_model: str = Field("llama3.2", alias="OLLAMA_MODEL")

    embeddings_model: str = Field(
        "sentence-transformers/all-MiniLM-L6-v2", alias="EMBEDDINGS_MODEL"
    )
    rag_top_k: int = Field(4, alias="RAG_TOP_K")

    app_env: str = Field("dev", alias="APP_ENV")


def get_settings() -> Settings:
    return Settings()
