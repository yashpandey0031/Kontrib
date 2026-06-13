import numpy as np
import faiss
import json
from pathlib import Path

INDEX_PATH = Path(__file__).resolve().parent / "knowledge_index.faiss"
CHUNKS_PATH = Path(__file__).resolve().parent / "knowledge_chunks.json"

class RAGEngine:
    def __init__(self):
        self.index = faiss.read_index(str(INDEX_PATH))
        with open(CHUNKS_PATH) as f:
            self.chunks = json.load(f)

    def retrieve(self, query: str, top_k: int = 3) -> list[str]:
        # use TF-IDF style keyword matching instead of embeddings
        query_words = set(query.lower().split())
        scores = []
        for chunk in self.chunks:
            chunk_words = set(chunk.lower().split())
            score = len(query_words & chunk_words)
            scores.append(score)
        
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        return [self.chunks[i] for i in top_indices]

rag_engine = RAGEngine()