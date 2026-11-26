"""Label retrieval results by hand (pooled, so it doesn't favour either retriever).

Run from backend/:   python eval/label_chunks.py
For each query it pools the top-5 chunks from BOTH retrievers, shuffles them
(you can't tell which retriever found what), and asks for a grade:
    2 = directly answers the query, 1 = partly relevant, 0 / Enter = irrelevant
Progress is saved after every query, so you can stop and resume.
"""
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from rag_engine import rag_engine  # noqa: E402

HERE = Path(__file__).resolve().parent
QUERIES = json.loads((HERE / "queries.json").read_text())
GOLDEN_PATH = HERE / "golden.json"
POOL_K = 5

golden = json.loads(GOLDEN_PATH.read_text()) if GOLDEN_PATH.exists() else {}
random.seed(0)

for qi, query in enumerate(QUERIES, 1):
    if query in golden:
        continue
    pool = list(dict.fromkeys(
        rag_engine.search_dense(query, POOL_K) + rag_engine.search_keyword(query, POOL_K)
    ))
    random.shuffle(pool)
    print(f"\n{'=' * 70}\n[{qi}/{len(QUERIES)}] QUERY: {query}\n{'=' * 70}")
    grades = {}
    for cid in pool:
        print(f"\n--- chunk {cid} ---\n{rag_engine.chunks[cid][:500]}")
        while True:
            g = input("grade (0/1/2, Enter=0): ").strip() or "0"
            if g in {"0", "1", "2"}:
                grades[str(cid)] = int(g)
                break
    golden[query] = grades
    GOLDEN_PATH.write_text(json.dumps(golden, indent=2))

print(f"\nDone. {len(golden)} queries labeled -> {GOLDEN_PATH}")
