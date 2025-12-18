from pydantic import BaseModel
from typing import Optional, List


class ChatRequest(BaseModel):
    question: str
    selected_text: Optional[str] = None  # If provided, answer only based on this text
    context: Optional[List[str]] = None  # Additional context to consider
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7


class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[str]] = None  # Module/section citations
    tokens_used: Optional[int] = None
    context_used: Optional[List[str]] = None  # Context that was used for the response


class SearchResponse(BaseModel):
    documents: List[str]
    scores: List[float]
    metadata: List[dict]