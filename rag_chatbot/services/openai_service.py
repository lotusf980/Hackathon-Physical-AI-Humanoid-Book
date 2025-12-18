from openai import OpenAI
from config.settings import settings
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


class OpenAIService:
    def __init__(self):
        if not settings.openai_api_key:
            logger.warning("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
            # Don't raise an error here - let the chat service handle it
            self.client = None
            self.model = settings.openai_model
        else:
            self.client = OpenAI(api_key=settings.openai_api_key)
            self.model = settings.openai_model
            logger.info(f"OpenAI service initialized with model: {self.model}")

    async def generate_response(
        self,
        question: str,
        context: Optional[List[str]] = None,
        selected_text: Optional[str] = None,
        sources: Optional[List[str]] = None,
        max_tokens: int = 1000,
        temperature: float = 0.3  # Lower temperature to reduce hallucination
    ) -> str:
        """
        Generate response using OpenAI Chat Completions API with RAG logic
        """
        try:
            # Check if OpenAI client is available
            if self.client is None:
                return "I'm sorry, but the OpenAI service is not properly configured. Please make sure the OPENAI_API_KEY environment variable is set."

            # Build the system message with context
            system_message = self._build_system_message(context, selected_text, sources)

            # Build the user message
            user_message = self._build_user_message(question, selected_text)

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return self._fallback_response(question)

    def _build_system_message(self, context: Optional[List[str]] = None, selected_text: Optional[str] = None, sources: Optional[List[str]] = None) -> str:
        """
        Build the system message with context for the RAG chatbot
        """
        base_message = (
            "You are a helpful assistant for the Physical AI & Humanoid Robotics textbook. "
            "You must answer questions based ONLY on the provided context. "
            "Do not make up information or hallucinate. "
            "If the context doesn't contain the answer, clearly state that you don't have enough information. "
            "Always cite the module/section where the information comes from. "
            "Be precise and accurate in your responses based on the provided context."
        )

        # If selected text is provided, restrict to only that text
        if selected_text:
            base_message += (
                "\n\nRESTRICTION: You must answer based ONLY on the following selected text. "
                "Do not use any other context or make assumptions beyond this text."
            )
            base_message += f"\n\nSELECTED TEXT: {selected_text}"
        # Otherwise, use the retrieved context from the book
        elif context:
            context_str = "\n\nRETRIEVED CONTEXT FROM BOOK:\n" + "\n".join([f"- {doc}" for doc in context[:5]])  # Limit to 5 documents
            base_message += context_str

            if sources:
                sources_str = "\n\nSOURCES (Module/Section): " + ", ".join(sources[:3])  # Limit to 3 sources
                base_message += sources_str
        else:
            base_message += (
                "\n\nNO CONTEXT PROVIDED: You do not have any relevant information to answer this question. "
                "State that you don't have enough information from the book to answer."
            )

        return base_message

    def _build_user_message(self, question: str, selected_text: Optional[str] = None) -> str:
        """
        Build the user message
        """
        if selected_text:
            return f"Question: {question}\n\nPlease answer based only on the selected text provided in the system message."
        return f"Question: {question}\n\nPlease answer based on the context provided in the system message and cite the relevant module/section."

    def _fallback_response(self, question: str) -> str:
        """
        Fallback response when OpenAI API is not available
        """
        return f"I'm having trouble processing your request. Could you rephrase your question: '{question}'?"