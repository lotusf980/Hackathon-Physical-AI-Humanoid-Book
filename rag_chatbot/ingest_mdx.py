#!/usr/bin/env python3
"""
RAG Ingestion Script for MDX Files

This script processes MDX files from the Docusaurus docs directory,
cleans the syntax, splits into semantic chunks, generates embeddings,
and stores them in Qdrant and Neon Postgres.
"""

import os
import re
import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from qdrant_client import QdrantClient
from qdrant_client.http import models
import asyncpg
from openai import OpenAI
import tiktoken
import frontmatter
from bs4 import BeautifulSoup
import hashlib
import uuid
from config.ingestion_config import settings


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class DocumentChunk:
    """Represents a semantic chunk of a document"""
    id: str
    content: str
    module: str
    file_path: str
    heading: str
    page_title: str
    chunk_index: int
    tokens: int


class MDXProcessor:
    """Processes MDX files to extract clean text content"""

    def __init__(self):
        self.enc = tiktoken.encoding_for_model("gpt-3.5-turbo")

    def clean_mdx_syntax(self, content: str) -> str:
        """Remove MDX-specific syntax while preserving content"""
        # Remove frontmatter
        content = re.sub(r'^---\n.*?---\n', '', content, flags=re.DOTALL)

        # Remove JSX components and expressions
        content = re.sub(r'<[^>]*>', '', content)  # Remove JSX tags
        content = re.sub(r'{[^}]*}', '', content)  # Remove JSX expressions

        # Remove markdown-style links but keep the text
        content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)

        # Remove image syntax
        content = re.sub(r'!\[[^\]]*\]\([^)]+\)', '', content)

        # Remove code blocks but preserve code content
        content = re.sub(r'```.*?\n(.*?)```', r'\1', content, flags=re.DOTALL)

        # Remove inline code backticks
        content = re.sub(r'`(.*?)`', r'\1', content)

        # Remove markdown formatting but keep text
        content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)  # Bold
        content = re.sub(r'\*(.*?)\*', r'\1', content)      # Italic
        content = re.sub(r'__(.*?)__', r'\1', content)      # Bold
        content = re.sub(r'_(.*?)_', r'\1', content)        # Italic

        # Remove markdown headers but keep the text
        content = re.sub(r'^#{1,6}\s+(.*)', r'\1', content, flags=re.MULTILINE)

        # Remove markdown lists
        content = re.sub(r'^\s*[-*+]\s+', '', content, flags=re.MULTILINE)
        content = re.sub(r'^\s*\d+\.\s+', '', content, flags=re.MULTILINE)

        # Remove markdown blockquotes
        content = re.sub(r'^\s*>\s+', '', content, flags=re.MULTILINE)

        # Clean up extra whitespace
        content = re.sub(r'\n\s*\n', '\n\n', content)  # Remove extra newlines
        content = re.sub(r'^\s+|\s+$', '', content, flags=re.MULTILINE)  # Trim lines

        return content.strip()

    def extract_frontmatter(self, file_path: Path) -> Tuple[Dict, str]:
        """Extract frontmatter and content from MDX file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        try:
            post = frontmatter.loads(content)
            return post.metadata, post.content
        except Exception as e:
            logger.warning(f"Could not parse frontmatter from {file_path}: {e}")
            # Fallback: try to extract title from first heading
            title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
            title = title_match.group(1) if title_match else file_path.stem
            return {'title': title}, re.sub(r'^---\n.*?---\n', '', content, flags=re.DOTALL)

    def get_token_count(self, text: str) -> int:
        """Get approximate token count for text"""
        return len(self.enc.encode(text))

    def split_into_chunks(self, content: str, max_tokens: int = 500) -> List[str]:
        """Split content into semantic chunks based on headings and paragraphs"""
        chunks = []
        paragraphs = content.split('\n\n')

        current_chunk = ""
        current_tokens = 0

        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue

            paragraph_tokens = self.get_token_count(paragraph)

            # If paragraph is too large, split it further
            if paragraph_tokens > max_tokens:
                sentences = re.split(r'[.!?]+\s+', paragraph)
                temp_chunk = ""

                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue

                    sentence_tokens = self.get_token_count(sentence)

                    if current_tokens + sentence_tokens > max_tokens and current_chunk:
                        chunks.append(current_chunk.strip())
                        current_chunk = sentence + ". "
                        current_tokens = sentence_tokens
                    elif len(temp_chunk) + len(sentence) > max_tokens:
                        if temp_chunk:
                            chunks.append(temp_chunk.strip())
                        temp_chunk = sentence + ". "
                    else:
                        temp_chunk += sentence + ". "

                if temp_chunk:
                    if current_tokens + self.get_token_count(temp_chunk) > max_tokens and current_chunk:
                        chunks.append(current_chunk.strip())
                        current_chunk = temp_chunk.strip()
                        current_tokens = self.get_token_count(temp_chunk)
                    else:
                        current_chunk += " " + temp_chunk.strip()
                        current_tokens += self.get_token_count(temp_chunk)
            else:
                # Check if adding this paragraph would exceed the token limit
                if current_tokens + paragraph_tokens > max_tokens and current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = paragraph
                    current_tokens = paragraph_tokens
                else:
                    if current_chunk:
                        current_chunk += "\n\n" + paragraph
                    else:
                        current_chunk = paragraph
                    current_tokens += paragraph_tokens

        # Add the last chunk if it exists
        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        return [chunk for chunk in chunks if chunk.strip() and self.get_token_count(chunk) > 10]


class EmbeddingService:
    """Service for generating embeddings"""

    def __init__(self, openai_api_key: str):
        self.client = OpenAI(api_key=openai_api_key)
        self.model = "text-embedding-ada-002"

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using OpenAI"""
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.model
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            # Return a zero vector as fallback
            return [0.0] * 1536


class VectorStoreService:
    """Service for storing vectors in Qdrant"""

    def __init__(self, qdrant_url: str, qdrant_api_key: str, collection_name: str):
        # Determine if it's a cloud URL (contains "cloud") or local
        is_cloud = "cloud" in qdrant_url.lower()

        try:
            if is_cloud and qdrant_api_key:
                # Cloud Qdrant setup
                self.client = QdrantClient(
                    url=qdrant_url,
                    api_key=qdrant_api_key,
                    https=True  # Qdrant Cloud uses HTTPS
                )
            else:
                # Local Qdrant setup (no API key needed)
                if qdrant_api_key:
                    self.client = QdrantClient(
                        url=qdrant_url,
                        api_key=qdrant_api_key
                    )
                else:
                    # Use in-memory storage for testing if local Qdrant isn't available
                    self.client = QdrantClient(":memory:")

            self.collection_name = collection_name
            self._ensure_collection_exists()
        except Exception as e:
            logger.warning(f"Could not connect to Qdrant: {e}. Using in-memory storage for testing.")
            # Fall back to in-memory storage
            self.client = QdrantClient(":memory:")
            self.collection_name = collection_name
            self._ensure_collection_exists()

    def _ensure_collection_exists(self):
        """Ensure the collection exists in Qdrant Cloud"""
        try:
            # Check if collection exists
            collections = self.client.get_collections()
            collection_exists = any(col.name == self.collection_name for col in collections.collections)

            if not collection_exists:
                # Create collection in Qdrant Cloud
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE)
                )
                logger.info(f"Created collection: {self.collection_name} in Qdrant Cloud")
            else:
                logger.info(f"Collection {self.collection_name} already exists in Qdrant Cloud")
        except Exception as e:
            logger.error(f"Error ensuring collection exists in Qdrant Cloud: {e}")
            raise

    def store_chunk(self, chunk: DocumentChunk, embedding: List[float]):
        """Store a document chunk in Qdrant"""
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=[
                    models.PointStruct(
                        id=chunk.id,
                        vector=embedding,
                        payload={
                            "content": chunk.content,
                            "module": chunk.module,
                            "file_path": str(chunk.file_path),
                            "heading": chunk.heading,
                            "page_title": chunk.page_title,
                            "chunk_index": chunk.chunk_index,
                            "tokens": chunk.tokens
                        }
                    )
                ]
            )
            logger.debug(f"Stored chunk {chunk.id} in Qdrant")
        except Exception as e:
            logger.error(f"Error storing chunk in Qdrant: {e}")
            raise


class DatabaseService:
    """Service for storing metadata in Neon Postgres"""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    async def initialize_tables(self):
        """Initialize required tables in Postgres - skip if no connection string provided"""
        if not self.connection_string:
            logger.info("No Postgres connection string provided, skipping table initialization")
            return

        conn = await asyncpg.connect(self.connection_string)
        try:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS document_chunks (
                    id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    module TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    heading TEXT,
                    page_title TEXT NOT NULL,
                    chunk_index INTEGER NOT NULL,
                    tokens INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create indexes for better query performance
            await conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_module ON document_chunks (module)
            ''')
            await conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_file_path ON document_chunks (file_path)
            ''')
            await conn.execute('''
                CREATE INDEX IF NOT EXISTS idx_heading ON document_chunks (heading)
            ''')

            logger.info("Database tables initialized")
        finally:
            await conn.close()

    async def store_chunk(self, chunk: DocumentChunk):
        """Store chunk metadata in Postgres - skip if connection unavailable"""
        if not self.connection_string:
            # Skip storing if no connection string provided
            logger.debug(f"Skipped storing chunk {chunk.id} in Postgres (no connection)")
            return

        try:
            conn = await asyncpg.connect(self.connection_string)
            try:
                await conn.execute('''
                    INSERT INTO document_chunks
                    (id, content, module, file_path, heading, page_title, chunk_index, tokens)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                    ON CONFLICT (id) DO UPDATE SET
                        content = EXCLUDED.content,
                        module = EXCLUDED.module,
                        file_path = EXCLUDED.file_path,
                        heading = EXCLUDED.heading,
                        page_title = EXCLUDED.page_title,
                        chunk_index = EXCLUDED.chunk_index,
                        tokens = EXCLUDED.tokens
                ''',
                    chunk.id, chunk.content, chunk.module, str(chunk.file_path),
                    chunk.heading, chunk.page_title, chunk.chunk_index, chunk.tokens
                )
                logger.debug(f"Stored chunk {chunk.id} in Postgres")
            finally:
                await conn.close()
        except Exception as e:
            logger.warning(f"Skipping Postgres storage for chunk {chunk.id}: {e}")
            # Continue without raising error - just store in vector DB


class MDXIngestor:
    """Main class for ingesting MDX files into RAG system"""

    def __init__(self, docs_dir: str, openai_api_key: str, qdrant_url: str,
                 qdrant_api_key: str, qdrant_collection: str, postgres_connection: str, chunk_max_tokens: int = 500):
        self.docs_dir = Path(docs_dir)
        self.chunk_max_tokens = chunk_max_tokens
        self.mdx_processor = MDXProcessor()
        self.embedding_service = EmbeddingService(openai_api_key)
        self.vector_store = VectorStoreService(qdrant_url, qdrant_api_key, qdrant_collection)
        self.db_service = DatabaseService(postgres_connection)

    async def initialize(self):
        """Initialize services"""
        if self.db_service.connection_string:  # Only initialize if connection string is provided
            try:
                await self.db_service.initialize_tables()
            except Exception as e:
                logger.warning(f"PostgreSQL initialization failed: {e}. Continuing with vector store only.")
                # Continue without Postgres - just use Qdrant for storage

    def extract_module_info(self, file_path: Path) -> str:
        """Extract module name from file path"""
        parts = file_path.parts
        for part in parts:
            if part.startswith('module'):
                return part
        return 'general'

    def extract_heading_from_content(self, content: str) -> str:
        """Extract the first heading from content"""
        heading_match = re.search(r'^#\s+(.+)$|^##\s+(.+)$|^###\s+(.+)$', content, re.MULTILINE)
        if heading_match:
            # Get the first non-None group
            heading = next((g for g in heading_match.groups() if g is not None), "")
            return heading.strip()
        return ""

    def get_page_title(self, metadata: Dict, file_path: Path) -> str:
        """Get page title from frontmatter or filename"""
        if 'title' in metadata and metadata['title']:
            return str(metadata['title'])
        return file_path.stem.replace('_', ' ').replace('-', ' ').title()

    async def process_file(self, file_path: Path) -> List[DocumentChunk]:
        """Process a single MDX file and return document chunks"""
        logger.info(f"Processing file: {file_path}")

        try:
            # Extract frontmatter and content
            metadata, content = self.mdx_processor.extract_frontmatter(file_path)

            # Clean MDX syntax
            clean_content = self.mdx_processor.clean_mdx_syntax(content)

            # Extract module info
            module = self.extract_module_info(file_path)

            # Get page title
            page_title = self.get_page_title(metadata, file_path)

            # Split into chunks
            chunks = self.mdx_processor.split_into_chunks(clean_content, self.chunk_max_tokens)

            doc_chunks = []
            for i, chunk_content in enumerate(chunks):
                chunk_id = str(uuid.uuid5(
                    uuid.NAMESPACE_DNS,
                    f"{file_path}_{i}_{hashlib.md5(chunk_content.encode()).hexdigest()}"
                ))

                chunk = DocumentChunk(
                    id=chunk_id,
                    content=chunk_content,
                    module=module,
                    file_path=file_path.relative_to(self.docs_dir),
                    heading=self.extract_heading_from_content(chunk_content),
                    page_title=page_title,
                    chunk_index=i,
                    tokens=self.mdx_processor.get_token_count(chunk_content)
                )

                doc_chunks.append(chunk)

            logger.info(f"Processed {file_path} into {len(doc_chunks)} chunks")
            return doc_chunks

        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            return []

    async def initialize(self):
        """Initialize services"""
        if self.db_service.connection_string:  # Only initialize if connection string is provided
            try:
                await self.db_service.initialize_tables()
            except Exception as e:
                logger.warning(f"PostgreSQL initialization failed: {e}. Continuing with vector store only.")
                # Continue without Postgres - just use Qdrant for storage

    async def ingest_directory(self):
        """Ingest all MDX files from the directory"""
        logger.info(f"Starting ingestion from directory: {self.docs_dir}")

        # Find all MDX files
        mdx_files = list(self.docs_dir.rglob("*.mdx"))
        logger.info(f"Found {len(mdx_files)} MDX files to process")

        total_chunks = 0

        for file_path in mdx_files:
            # Process the file
            document_chunks = await self.process_file(file_path)

            # Process each chunk
            for chunk in document_chunks:
                try:
                    # Generate embedding
                    embedding = self.embedding_service.generate_embedding(chunk.content)

                    # Store in vector store
                    self.vector_store.store_chunk(chunk, embedding)

                    # Store in database
                    await self.db_service.store_chunk(chunk)

                    total_chunks += 1

                except Exception as e:
                    logger.error(f"Error processing chunk {chunk.id} from {file_path}: {e}")

        logger.info(f"Ingestion completed. Processed {total_chunks} chunks from {len(mdx_files)} files.")


async def main():
    """Main function to run the ingestion process"""
    # Use configuration from environment variables
    if not settings.openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    if not settings.postgres_connection:
        raise ValueError("POSTGRES_CONNECTION environment variable is required")

    ingestor = MDXIngestor(
        docs_dir=settings.docs_dir,
        openai_api_key=settings.openai_api_key,
        qdrant_url=settings.qdrant_url,
        qdrant_api_key=settings.qdrant_api_key,
        qdrant_collection=settings.qdrant_collection,
        postgres_connection=settings.postgres_connection,
        chunk_max_tokens=settings.chunk_max_tokens
    )

    asyncio.run(ingestor.initialize())
    asyncio.run(ingestor.ingest_directory())


if __name__ == "__main__":
    asyncio.run(main())