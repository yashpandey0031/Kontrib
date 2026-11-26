import json
from pathlib import Path

import faiss
import numpy as np
from fastembed import TextEmbedding

KNOWLEDGE_BASE_DIR = Path("../knowledge_base")
OUTPUT_DIR = Path(".")
MODEL_NAME = "BAAI/bge-small-en-v1.5"  # must match rag_engine.py

model = TextEmbedding(MODEL_NAME)

chunks = []
# sorted() keeps chunk order identical on every OS
for file in sorted(KNOWLEDGE_BASE_DIR.glob("*.md")):
    text = file.read_text(encoding="utf-8")
    paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 50]
    chunks.extend(paragraphs)

print(f"Building index for {len(chunks)} chunks...")
embeddings = np.array(list(model.embed(chunks)), dtype=np.float32)
faiss.normalize_L2(embeddings)  # inner product == cosine similarity

index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, str(OUTPUT_DIR / "knowledge_index.faiss"))
with open(OUTPUT_DIR / "knowledge_chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f)

print("Done. Commit knowledge_index.faiss and knowledge_chunks.json together.")
