import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # OpenAI settings
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

    # Qdrant Cloud settings
    qdrant_url: str = os.getenv("QDRANT_URL", "https://098fd0bc-60ee-42c1-9df1-bd0360ebf263.europe-west3-0.gcp.cloud.qdrant.io:6333")
    qdrant_api_key: str = os.getenv("QDRANT_API_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.smHamioZMRkKd0GwrFUr-MJW2uGLpmYrC3IF10p3LK0")
    qdrant_collection: str = os.getenv("QDRANT_COLLECTION", "Physical-AI-Book")

    # Application settings
    app_name: str = "RAG Chatbot API"
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", 8000))

    class Config:
        env_file = ".env"


settings = Settings()