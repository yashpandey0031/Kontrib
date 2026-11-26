import os

from dotenv import load_dotenv
from groq import Groq

from rag_engine import rag_engine

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "openai/gpt-oss-20b"

# One retrieval query per metric, so the context depends on what the user is
# actually weak at. eval/queries.json mirrors this style.
METRIC_QUERIES = {
    "avg_message_length": "writing descriptive commit messages with enough context",
    "conventional_commit_rate": "conventional commits format with feat fix docs prefixes",
    "multiline_rate": "commit message body explaining why the change was made",
}
DEFAULT_QUERY = "how to write good commit messages"


def retrieve_context(metrics_comparison: dict, per_metric_k: int = 2, max_chunks: int = 5) -> list[str]:
    weak = [
        name for name, m in metrics_comparison.items()
        if name in METRIC_QUERIES and m["rating"] != "good"
    ]
    queries = [METRIC_QUERIES[n] for n in weak] or [DEFAULT_QUERY]

    seen, context = set(), []
    for q in queries:
        for chunk in rag_engine.retrieve(q, top_k=per_metric_k):
            if chunk not in seen:
                seen.add(chunk)
                context.append(chunk)
    return context[:max_chunks]


def analyze_with_llm(
    username: str,
    user_messages: list,
    benchmark_username: str,
    benchmark_messages: list,
    metrics_comparison: dict,
) -> str:

    if all(v["rating"] == "good" for v in metrics_comparison.values()):
        return "All metrics match or exceed the benchmark. Your commit style aligns well with top contributors in this repo."

    context_text = "\n\n".join(retrieve_context(metrics_comparison))

    prompt = f"""
You are a senior code contribution analyst. Analyze {username}'s commit style and compare it to {benchmark_username}.
Format your response in clean bullet points. Keep total response under 200 words.

{username}'s actual commit messages:
{chr(10).join(f'- {m[:100]}' for m in user_messages[:10])}

{benchmark_username}'s commit messages (benchmark):
{chr(10).join(f'- {m[:100]}' for m in benchmark_messages[:10])}

Metrics:
- Avg message length: {username} = {metrics_comparison['avg_message_length']['your_value']} chars, {benchmark_username} = {metrics_comparison['avg_message_length']['benchmark_value']} chars
- Conventional commit rate: {username} = {metrics_comparison['conventional_commit_rate']['your_value']}, {benchmark_username} = {metrics_comparison['conventional_commit_rate']['benchmark_value']}
- Multiline rate: {username} = {metrics_comparison['multiline_rate']['your_value']}, {benchmark_username} = {metrics_comparison['multiline_rate']['benchmark_value']}

Best practises references:
{context_text}


Based ONLY on {username}'s messages above, provide:
1. Honest assessment of {username}'s commit style (2-3 sentences)
2. Three specific improvements with examples from {username}'s ACTUAL messages
3. One thing {username} is doing well

Be specific. Only reference {username}'s messages in examples, not {benchmark_username}'s.
Reference the best practices above where relevant.

"""

    response = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content


# if groq is not available
def analyze_fallback(metrics_comparison: dict) -> str:
    insights = []

    msg_len = metrics_comparison["avg_message_length"]
    if msg_len["rating"] == "below benchmark":
        insights.append(f"Your commit messages average {msg_len['your_value']} chars vs {msg_len['benchmark_value']} for top contributors. Add more context.")

    conv = metrics_comparison["conventional_commit_rate"]
    if conv["your_value"] == 0:
        insights.append("You don't use conventional commits (feat:/fix:/docs:). Start using them for clarity.")

    multi = metrics_comparison["multiline_rate"]
    if multi["rating"] == "below benchmark":
        insights.append("Add multi-line commit messages explaining WHY you made the change, not just what.")

    return " ".join(insights) if insights else "Your commit style looks good!"
