
import numpy as np
import os
from pathlib import Path
os.environ["SENTENCE_TRANSFORMERS_HOME"] = str(Path(__file__).resolve().parent / ".cache" / "models")
os.environ["HF_HOME"] = str(Path(__file__).resolve().parent / ".cache" / "hf")
import faiss
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
KNOWLEDGE_BASE_DIR = Path(__file__).resolve().parent.parent / "knowledge_base"


class RAGEngine:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)
        self.chunks = []
        self.index = None
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        for file in KNOWLEDGE_BASE_DIR.glob("*.md"):
            text = file.read_text(encoding="utf-8")
            paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 50]
            self.chunks.extend(paragraphs)

        # outside the loop
        embeddings = self.model.encode(self.chunks, normalize_embeddings=True)
        embeddings = np.array(embeddings, dtype=np.float32)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

    def retrieve(self, query: str, top_k: int = 3) -> list[str]:
        query_vec = self.model.encode([query], normalize_embeddings=True)
        query_vec = np.array(query_vec, dtype=np.float32)
        scores, indices = self.index.search(query_vec, k=top_k)
        return [self.chunks[i] for i in indices[0] if i < len(self.chunks)]

rag_engine = RAGEngine()