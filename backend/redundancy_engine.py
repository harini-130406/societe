import numpy as np
from sentence_transformers import SentenceTransformer

# Lazy loading of embeddings model
_embedder = None

def get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
    return _embedder

def calculate_similarity(text_a: str, text_b: str) -> float:
    """
    Computes cosine similarity between two sentences using Sentence Transformers.
    """
    embedder = get_embedder()
    embeddings = embedder.encode([text_a, text_b], show_progress_bar=False)
    
    emb_a = embeddings[0]
    emb_b = embeddings[1]
    
    # Cosine similarity
    similarity = np.dot(emb_a, emb_b) / (np.linalg.norm(emb_a) * np.linalg.norm(emb_b))
    return float(similarity)
