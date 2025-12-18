from fastapi import APIRouter, HTTPException, Depends
from models.chat import ChatRequest, ChatResponse
from services.chat_service import ChatService
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize the chat service
chat_service = ChatService()


@router.post("/chat", response_model=ChatResponse, summary="Chat with RAG bot")
async def chat_endpoint(request: ChatRequest):
    """
    Process a chat request using Retrieval-Augmented Generation.

    - **question**: The user's question
    - **selected_text**: Optional selected text to provide additional context
    - **context**: Optional list of context strings
    - **max_tokens**: Maximum number of tokens in the response (default: 1000)
    - **temperature**: Creativity of the response (default: 0.7)
    """
    try:
        logger.info(f"Processing chat request: {request.question[:50]}...")

        # Process the chat request using the service
        response = await chat_service.process_chat(request)

        logger.info("Chat request processed successfully")
        return response

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))