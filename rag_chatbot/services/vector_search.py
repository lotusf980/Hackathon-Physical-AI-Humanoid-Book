from typing import List, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models
from config.settings import settings
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)


class VectorSearchService:
    def __init__(self):
        try:
            # Connect to Qdrant Cloud
            self.client = QdrantClient(
                url=settings.qdrant_url,
                api_key=settings.qdrant_api_key,
                https=True  # Qdrant Cloud uses HTTPS
            )
            self.collection_name = settings.qdrant_collection
            logger.info(f"Connected to Qdrant Cloud at {settings.qdrant_url}")

            # Initialize OpenAI client for embedding generation
            if not settings.openai_api_key:
                logger.warning("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
                self.openai_client = None
            else:
                self.openai_client = OpenAI(api_key=settings.openai_api_key)
                logger.info("OpenAI client initialized for embeddings")

        except Exception as e:
            logger.error(f"Failed to initialize VectorSearchService: {e}")
            logger.error(f"Qdrant URL: {settings.qdrant_url}")
            logger.error(f"Qdrant collection: {settings.qdrant_collection}")
            logger.error(f"OpenAI API key set: {bool(settings.openai_api_key)}")

            # Fallback to mock implementation
            self.client = None
            self.openai_client = None

    async def search(self, query: str, top_k: int = 5) -> List[dict]:
        """
        Search for similar documents in the vector database using vector similarity search
        """
        if self.client is None or self.openai_client is None:
            # Mock implementation for development
            return self._mock_search(query, top_k)

        try:
            # Generate embedding for the query
            response = self.openai_client.embeddings.create(
                input=query,
                model="text-embedding-ada-002"
            )
            query_embedding = response.data[0].embedding

            # Perform vector search in Qdrant
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=top_k,
                with_payload=True
            )

            results = []
            for result in search_results:
                results.append({
                    'id': result.id,
                    'document': result.payload.get('content', ''),
                    'score': result.score,
                    'metadata': result.payload
                })

            return results
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return self._mock_search(query, top_k)

    def _mock_search(self, query: str, top_k: int = 5) -> List[dict]:
        """
        Mock search implementation for development without Qdrant Cloud
        """
        # This is a simple mock - in real implementation, you'd use proper vector search
        mock_docs = [
            {"id": "1", "content": f"Relevant document about {query}", "score": 0.9, "metadata": {"source": "doc1.pdf", "module": "general"}},
            {"id": "2", "content": f"Another document related to {query}", "score": 0.8, "metadata": {"source": "doc2.pdf", "module": "general"}},
            {"id": "3", "content": f"Information about {query} in context", "score": 0.7, "metadata": {"source": "doc3.pdf", "module": "general"}},
            {"id": "4", "content": f"Additional context for {query}", "score": 0.6, "metadata": {"source": "doc4.pdf", "module": "general"}},
            {"id": "5", "content": f"Supporting information about {query}", "score": 0.5, "metadata": {"source": "doc5.pdf", "module": "general"}},
        ]
        return mock_docs[:top_k]

    async def add_document(self, doc_id: str, content: str, metadata: dict = None):
        """
        Add a document to the vector database with proper embedding
        """
        if self.client is None or self.openai_client is None:
            logger.warning("Qdrant Cloud or OpenAI not available, skipping document addition")
            return

        try:
            # Generate embedding for the content
            response = self.openai_client.embeddings.create(
                input=content,
                model="text-embedding-ada-002"
            )
            embedding = response.data[0].embedding

            # Upsert the document with its embedding
            self.client.upsert(
                collection_name=self.collection_name,
                points=[models.PointStruct(
                    id=doc_id,
                    vector=embedding,
                    payload={
                        "content": content,
                        **(metadata or {})
                    }
                )]
            )
            logger.info(f"Added document {doc_id} to Qdrant Cloud")
        except Exception as e:
            logger.error(f"Failed to add document to Qdrant Cloud: {e}")

    async def batch_add_documents(self, documents: List[dict]):
        """
        Add multiple documents to the vector database efficiently
        """
        if self.client is None or self.openai_client is None:
            logger.warning("Qdrant Cloud or OpenAI not available, skipping batch document addition")
            return

        try:
            # Prepare points for batch insertion
            points = []

            for doc in documents:
                doc_id = doc['id']
                content = doc['content']
                metadata = doc.get('metadata', {})

                # Generate embedding for the content
                response = self.openai_client.embeddings.create(
                    input=content,
                    model="text-embedding-ada-002"
                )
                embedding = response.data[0].embedding

                points.append(models.PointStruct(
                    id=doc_id,
                    vector=embedding,
                    payload={
                        "content": content,
                        **metadata
                    }
                ))

            # Batch upsert documents
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            logger.info(f"Added {len(documents)} documents to Qdrant Cloud")
        except Exception as e:
            logger.error(f"Failed to batch add documents to Qdrant Cloud: {e}")