import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant"

def analyze_with_llm(
    username: str,
    user_messages: list,
    benchmark_username: str,
    benchmark_messages: list,
    metrics_comparison: dict,
) -> str:
  
  prompt = f""" 
you are a code contribution analyst , compare two developers' commit message styles.

Developer being analyzed: {username}
Their commit messages (sample):
{chr(10).join(f'- {m[:100]}' for m in user_messages[:10])}

Benchmark developer: {benchmark_messages}
Their commit messages (sample):
{chr(10).join(f'- {m[:100]}' for m in benchmark_messages[:10])}

Metrics comaprison:
- Average message length: {username} wrote {metrics_comparison['avg_message_length']['your_value']} chars vs {metrics_comparison['avg_message_length']['benchmark_value']} chars
- Conventional commit rate: {metrics_comparison['conventional_commit_rate']['your_value']} vs {metrics_comparison['conventional_commit_rate']['benchmark_value']}
- Multiline rate: {metrics_comparison['multiline_rate']['your_value']} vs {metrics_comparison['multiline_rate']['benchmark_value']}

Provide:
1. A brief honest assessment of {username}'s commit style (2-3 sentences)
2. Three specific improvements they should make with examples
3. One thing they are doing well

Keep it concise, specific, and actionable. No fluff.
"""
  
  response  =client.chat.completions.create(model = MODEL,messages= [{"role":"user","content":prompt}])

  return response.choices[0].message.content

#if groq is not avaible 
def analyze_fallback(metrics_comparison: dict) -> str:
    insights = []
    
    msg_len = metrics_comparison['avg_message_length']
    if msg_len['rating'] == 'below benchmark':
        insights.append(f"Your commit messages average {msg_len['your_value']} chars vs {msg_len['benchmark_value']} for top contributors. Add more context.")
    
    conv = metrics_comparison['conventional_commit_rate']
    if conv['your_value'] == 0:
        insights.append("You don't use conventional commits (feat:/fix:/docs:). Start using them for clarity.")
    
    multi = metrics_comparison['multiline_rate']
    if multi['rating'] == 'below benchmark':
        insights.append("Add multi-line commit messages explaining WHY you made the change, not just what.")
    
    return " ".join(insights) if insights else "Your commit style looks good!"