
import json
from pathlib import Path

KNOWLEDGE_BASE_DIR = Path("../knowledge_base")
chunks = []

for file in KNOWLEDGE_BASE_DIR.glob("*.md"):
    text = file.read_text(encoding="utf-8")
    paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 50]
    chunks.extend(paragraphs)

with open("knowledge_chunks.json", "w") as f:
    json.dump(chunks, f)

print(f"Saved {len(chunks)} chunks")