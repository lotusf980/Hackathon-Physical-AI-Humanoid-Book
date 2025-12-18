#!/usr/bin/env python3
"""
Script to run MDX ingestion for the Physical AI & Humanoid Robotics book
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, str(Path(__file__).parent))

from ingest_mdx import MDXIngestor
from config.ingestion_config import settings


def run_ingestion():
    """Run the MDX ingestion process with project-specific settings"""

    # Set environment variables for the ingestion before loading settings
    os.environ.setdefault('DOCS_DIR', str(Path(__file__).parent.parent / "docs"))  # Point to the actual docs directory
    os.environ.setdefault('QDRANT_URL', 'https://098fd0bc-60ee-42c1-9df1-bd0360ebf263.europe-west3-0.gcp.cloud.qdrant.io:6333')
    os.environ.setdefault('QDRANT_API_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.smHamioZMRkKd0GwrFUr-MJW2uGLpmYrC3IF10p3LK0')
    os.environ.setdefault('QDRANT_COLLECTION', 'Physical-AI-Book')
    os.environ.setdefault('OPENAI_API_KEY', os.getenv('OPENAI_API_KEY', ''))  # Preserve any existing OPENAI_API_KEY
    os.environ.setdefault('POSTGRES_CONNECTION', os.getenv('POSTGRES_CONNECTION', ''))  # Preserve any existing POSTGRES_CONNECTION

    # Reload settings to pick up new environment variables
    from config.ingestion_config import IngestionSettings
    settings = IngestionSettings()

    print(f"Starting MDX ingestion process...")
    print(f"Processing docs from: {settings.docs_dir}")
    print(f"Qdrant collection: {settings.qdrant_collection}")
    print(f"PostgreSQL connection: {'SET' if settings.postgres_connection else 'NOT SET'}")
    print(f"OpenAI API key: {'SET' if settings.openai_api_key else 'NOT SET'}")

    # Verify the docs directory exists and list MDX files
    docs_path = Path(settings.docs_dir)
    if not docs_path.exists():
        print(f"ERROR: Docs directory does not exist: {settings.docs_dir}")
        return

    mdx_files = list(docs_path.rglob("*.mdx"))
    print(f"Found {len(mdx_files)} MDX files to process")
    for file in mdx_files:
        print(f"  - {file}")

    if not settings.openai_api_key:
        print("\n[WARNING] OPENAI_API_KEY environment variable is not set.")
        print("The ingestion will run but embeddings won't be generated properly.")
        print("Please set OPENAI_API_KEY to generate proper embeddings.\n")

    if not settings.postgres_connection:
        print("\n[WARNING] POSTGRES_CONNECTION environment variable is not set.")
        print("Only Qdrant vector store will be populated.\n")

    try:
        # Create the ingestor with settings
        ingestor = MDXIngestor(
            docs_dir=settings.docs_dir,
            openai_api_key=settings.openai_api_key,
            qdrant_url=settings.qdrant_url,
            qdrant_api_key=settings.qdrant_api_key,
            qdrant_collection=settings.qdrant_collection,
            postgres_connection=settings.postgres_connection,
            chunk_max_tokens=settings.chunk_max_tokens
        )

        # Initialize and run the ingestion
        asyncio.run(ingestor.initialize())
        asyncio.run(ingestor.ingest_directory())
        print("\nSUCCESS: Ingestion completed successfully!")

    except Exception as e:
        print(f"\nERROR: Error during ingestion: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_ingestion()