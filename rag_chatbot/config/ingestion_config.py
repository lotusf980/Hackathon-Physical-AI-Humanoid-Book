import os
from pydantic_settings import BaseSettings


class IngestionSettings(BaseSettings):
    # Source directory
    docs_dir: str = os.getenv("DOCS_DIR", "docs")

    # OpenAI settings
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    # Qdrant Cloud settings
    qdrant_url: str = os.getenv("QDRANT_URL", "https://098fd0bc-60ee-42c1-9df1-bd0360ebf263.europe-west3-0.gcp.cloud.qdrant.io:6333")  # Qdrant Cloud URL
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.smHamioZMRkKd0GwrFUr-MJW2uGLpmYrC3IF10p3LK0")  # Qdrant Cloud API key
    qdrant_collection: str = os.getenv("QDRANT_COLLECTION", "Physical-AI-Book")

    # Postgres settings
    postgres_connection: str = os.getenv("POSTGRES_CONNECTION", "")

    # Processing settings
    chunk_max_tokens: int = int(os.getenv("CHUNK_MAX_TOKENS", 500))

    class Config:
        env_file = ".env"


settings = IngestionSettings()