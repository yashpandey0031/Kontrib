import asyncio
import json
from github_client import get_user, get_user_commits, get_top_contributors

def analyze_commits(commits: list) -> dict:
  messages=[c["commit"]["message"] for c in commits]

  total_commits= len(commits)

  avg_message_length = sum(len(m) for m in messages) / len(messages)

  PREFIXES = ["feat:", "fix:", "docs:", "chore:", "refactor:", "test:"]

  conventional_commit_rate = sum(1 for m in messages if any(m.startswith(p) for p in PREFIXES))
  rate = conventional_commit_rate / len(messages)

  multiline = sum(1 for m in messages if "\n" in m)
  rate_miltline = multiline / len(messages)

  return {
    "total_Commits" : total_commits,
    "avg_message_length" : round(avg_message_length,2),
    "conventional_commit_Rate" : round(conventional_commit_rate,2),
    "multiline_Rate" : round(rate_miltline,2),
  }