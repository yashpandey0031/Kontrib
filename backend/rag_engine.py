import json
from pathlib import Path

import faiss
import numpy as np
from fastembed import TextEmbedding

BASE_DIR = Path(__file__).resolve().parent
INDEX_PATH = BASE_DIR / "knowledge_index.faiss"
CHUNKS_PATH = BASE_DIR / "knowledge_chunks.json"
MODEL_NAME = "BAAI/bge-small-en-v1.5"  # must match build_index.py


class RAGEngine:
    def __init__(self):
        self.index = faiss.read_index(str(INDEX_PATH))
        with open(CHUNKS_PATH, encoding="utf-8") as f:
            self.chunks = json.load(f)
        # If this fails, the index and chunks file were built at different
        # times. Re-run build_index.py (it writes both together).
        assert self.index.ntotal == len(self.chunks), (
            f"index has {self.index.ntotal} vectors but {len(self.chunks)} chunks"
        )
        self.model = TextEmbedding(MODEL_NAME)

    # ---- dense (FAISS) retrieval: what the resume bullet claims ----
    def search_dense(self, query: str, top_k: int = 3) -> list[int]:
        q = np.array(list(self.model.embed([query])), dtype=np.float32)
        faiss.normalize_L2(q)
        _, ids = self.index.search(q, top_k)
        return [int(i) for i in ids[0] if i != -1]

    # ---- old keyword-overlap retrieval, kept ONLY as the eval baseline ----
    def search_keyword(self, query: str, top_k: int = 3) -> list[int]:
        query_words = set(query.lower().split())
        scores = [len(query_words & set(c.lower().split())) for c in self.chunks]
        return sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]

    def retrieve(self, query: str, top_k: int = 3) -> list[str]:
        return [self.chunks[i] for i in self.search_dense(query, top_k)]


rag_engine = RAGEngine()
