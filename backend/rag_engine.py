import numpy as np
import os
import faiss
from pathlib import Path
from fastembed import TextEmbedding

os.environ["HF_HOME"] = str(Path(__file__).resolve().parent / ".cache" / "hf")

KNOWLEDGE_BASE_DIR = Path(__file__).resolve().parent.parent / "knowledge_base"


class RAGEngine:
    def __init__(self):
        self.model = TextEmbedding("BAAI/bge-small-en-v1.5")
        self.chunks = []
        self.index = None
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        for file in KNOWLEDGE_BASE_DIR.glob("*.md"):
            text = file.read_text(encoding="utf-8")
            paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 50]
            self.chunks.extend(paragraphs)

        embeddings = np.array(list(self.model.embed(self.chunks)), dtype=np.float32)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(embeddings)

    def retrieve(self, query: str, top_k: int = 3) -> list[str]:
        query_vec = np.array(list(self.model.embed([query])), dtype=np.float32)
        scores, indices = self.index.search(query_vec, k=top_k)
        return [self.chunks[i] for i in indices[0] if i < len(self.chunks)]


rag_engine = RAGEngine()