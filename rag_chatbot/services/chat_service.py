from typing import Optional, List
from services.vector_search import VectorSearchService
from services.openai_service import OpenAIService
from models.chat import ChatRequest, ChatResponse
import logging

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self):
        try:
            from .vector_search import VectorSearchService
            from .openai_service import OpenAIService

            self.vector_search = VectorSearchService()
            self.openai_service = OpenAIService()
            logger.info("ChatService initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ChatService: {e}")
            # Import services here to avoid circular imports
            from .vector_search import VectorSearchService
            from .openai_service import OpenAIService

            self.vector_search = VectorSearchService()
            # We'll handle OpenAI service error in the process_chat method
            try:
                self.openai_service = OpenAIService()
            except ValueError:
                logger.error("OpenAI service could not be initialized due to missing API key")
                self.openai_service = None

    async def process_chat(self, request: ChatRequest) -> ChatResponse:
        """
        Process a chat request using RAG (Retrieval-Augmented Generation) with following logic:
        - If user provides selected text, restrict answers to that text only
        - Otherwise answer using full book knowledge (retrieved from Qdrant)
        - Prevent hallucination by restricting to provided context
        - Cite module/section in response
        """
        try:
            # Check if services are properly initialized
            if self.openai_service is None:
                return ChatResponse(
                    response="I'm sorry, but the OpenAI service is not properly configured. Please make sure the OPENAI_API_KEY environment variable is set.",
                    sources=[],
                    tokens_used=0
                )

            # Determine context based on selected_text presence
            context_docs = []
            sources = []

            if request.selected_text:
                # If selected text is provided, use only that text as context
                context_docs = [request.selected_text]
                sources = ["Selected Text Only"]  # Indicate that response is restricted to selected text
                logger.info("Using selected text as context only")
            else:
                # Otherwise, retrieve top-k chunks from Qdrant based on the question
                search_results = await self.vector_search.search(
                    query=request.question,
                    top_k=5
                )

                # Extract document content for context
                context_docs = [result['document'] for result in search_results if result['document']]

                # Extract sources (module/section info) from metadata
                for result in search_results:
                    metadata = result['metadata']
                    # Create a readable source identifier combining module and file info
                    module = metadata.get('module', 'general')
                    file_path = metadata.get('file_path', 'unknown')
                    heading = metadata.get('heading', '')

                    source_info = f"{module}"
                    if file_path != 'unknown':
                        source_info += f"/{file_path}"
                    if heading:
                        source_info += f" - {heading}"

                    sources.append(source_info)

                # Include any provided context from the request
                if request.context:
                    context_docs.extend(request.context)

                logger.info(f"Retrieved {len(context_docs)} context chunks from Qdrant Cloud")

            # Generate response using OpenAI with the determined context
            response_text = await self.openai_service.generate_response(
                question=request.question,
                context=context_docs,
                selected_text=request.selected_text,  # Pass selected_text to OpenAI service
                sources=sources,
                max_tokens=request.max_tokens,
                temperature=0.3  # Lower temperature to reduce hallucination
            )

            # Prepare the response
            return ChatResponse(
                response=response_text,
                sources=sources,
                context_used=context_docs[:3],  # Return first 3 context documents
                tokens_used=len(response_text.split())  # Rough token count
            )

        except Exception as e:
            logger.error(f"Error processing chat: {e}")
            logger.exception("Full exception traceback:")  # Log the full traceback

            # Check if the error is related to missing API keys
            if "OPENAI_API_KEY" in str(e) or "OpenAI API key" in str(e):
                return ChatResponse(
                    response="I'm sorry, but the OpenAI service is not properly configured. Please make sure the OPENAI_API_KEY environment variable is set.",
                    sources=[],
                    tokens_used=0
                )

            return ChatResponse(
                response="I'm sorry, I encountered an error processing your request. Please try again.",
                sources=[],
                tokens_used=0
            )