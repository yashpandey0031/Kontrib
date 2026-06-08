from rag_engine import rag_engine

results = rag_engine.retrieve("how to write good commit messages")
for r in results:
    print(r)
    print("---")