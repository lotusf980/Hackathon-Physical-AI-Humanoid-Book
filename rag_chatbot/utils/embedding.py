from typing import List
import numpy as np
from config.settings import settings


class EmbeddingService:
    def __init__(self):
        # In a real implementation, you'd initialize an embedding model here
        # e.g., using OpenAI, SentenceTransformers, etc.
        self.embedding_dim = 1536  # Default for OpenAI ada-002

    def create_embedding(self, text: str) -> List[float]:
        """
        Create an embedding for the given text.
        In a real implementation, this would call an embedding API or model.
        """
        # Placeholder implementation - in real scenario, use actual embedding model
        # For now, we'll return a deterministic pseudo-embedding based on text
        import hashlib
        hash_input = text.encode('utf-8')
        hash_value = int(hashlib.md5(hash_input).hexdigest(), 16)

        # Create a deterministic vector based on the hash
        np.random.seed(hash_value % (2**32 - 1))  # Use hash as seed
        embedding = np.random.random(self.embedding_dim).tolist()

        return embedding

    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Create embeddings for a list of texts
        """
        return [self.create_embedding(text) for text in texts]

    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors
        """
        import numpy as np
        v1 = np.array(vec1)
        v2 = np.array(vec2)

        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)

        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0

        return float(dot_product / (norm_v1 * norm_v2))