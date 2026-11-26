"""Compare keyword vs FAISS retrieval on your hand-labeled golden set.

Run from backend/:   python eval/run_eval.py
Prints Hit@k, Recall@k, MRR and nDCG@k, and saves a timestamped JSON of results.
"""
import json
import math
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

HERE = Path(__file__).resolve().parent
K = 3


def hit_at_k(ranked, grades, k):
    return float(any(grades.get(str(c), 0) > 0 for c in ranked[:k]))


def recall_at_k(ranked, grades, k):
    relevant = {c for c, g in grades.items() if g > 0}
    if not relevant:
        return None
    return len({str(c) for c in ranked[:k]} & relevant) / len(relevant)


def mrr(ranked, grades):
    for i, c in enumerate(ranked, 1):
        if grades.get(str(c), 0) > 0:
            return 1.0 / i
    return 0.0


def ndcg_at_k(ranked, grades, k):
    dcg = sum(grades.get(str(c), 0) / math.log2(i + 2) for i, c in enumerate(ranked[:k]))
    ideal = sorted(grades.values(), reverse=True)[:k]
    idcg = sum(g / math.log2(i + 2) for i, g in enumerate(ideal))
    return dcg / idcg if idcg > 0 else None


def evaluate(search_fn, golden, k=K):
    rows, latencies = [], []
    for query, grades in golden.items():
        if not any(g > 0 for g in grades.values()):
            continue  # no relevant chunk exists for this query; skip it
        t0 = time.perf_counter()
        ranked = search_fn(query, k)
        latencies.append((time.perf_counter() - t0) * 1000)
        rows.append({
            "hit": hit_at_k(ranked, grades, k),
            "recall": recall_at_k(ranked, grades, k),
            "mrr": mrr(ranked, grades),
            "ndcg": ndcg_at_k(ranked, grades, k),
        })
    avg = lambda key: sum(r[key] for r in rows) / len(rows)
    return {
        f"Hit@{k}": avg("hit"), f"Recall@{k}": avg("recall"),
        "MRR": avg("mrr"), f"nDCG@{k}": avg("ndcg"),
        "avg_latency_ms": sum(latencies) / len(latencies),
        "n_queries": len(rows),
    }


def main():
    from rag_engine import rag_engine  # imported here so the metrics above are testable alone

    golden = json.loads((HERE / "golden.json").read_text())
    results = {
        "keyword (old)": evaluate(rag_engine.search_keyword, golden),
        "FAISS dense (new)": evaluate(rag_engine.search_dense, golden),
    }
    cols = list(next(iter(results.values())))
    print(f"\n{'retriever':<20}" + "".join(f"{c:>15}" for c in cols))
    for name, r in results.items():
        print(f"{name:<20}" + "".join(f"{r[c]:>15.3f}" if c != "n_queries" else f"{r[c]:>15d}" for c in cols))

    out = HERE / f"results_{datetime.now():%Y%m%d_%H%M%S}.json"
    out.write_text(json.dumps(results, indent=2))
    print(f"\nSaved -> {out}")


if __name__ == "__main__":
    main()
