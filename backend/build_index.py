
import numpy as np
import faiss
import json
from pathlib import Path
from fastembed import TextEmbedding

KNOWLEDGE_BASE_DIR = Path("../knowledge_base")
OUTPUT_DIR = Path(".")

model = TextEmbedding("BAAI/bge-small-en-v1.5")

chunks = []
for file in KNOWLEDGE_BASE_DIR.glob("*.md"):
    text = file.read_text(encoding="utf-8")
    paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 50]
    chunks.extend(paragraphs)

print(f"Building index for {len(chunks)} chunks...")
embeddings = np.array(list(model.embed(chunks)), dtype=np.float32)

index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, str(OUTPUT_DIR / "knowledge_index.faiss"))
with open(OUTPUT_DIR / "knowledge_chunks.json", "w") as f:
    json.dump(chunks, f)

print("Done. Commit knowledge_index.faiss and knowledge_chunks.json")