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
    "total_commits" : total_commits,
    "avg_message_length" : round(avg_message_length,2),
    "conventional_commit_rate" : round(conventional_commit_rate,2),
    "multiline_rate" : round(rate_miltline,2),
  }


def compare(user_mertrics: dict, benchmark_metrics: dict) -> dict:
  results = {}

  for metric in user_mertrics:
    user_val = user_mertrics[metric] #metric for that user and that metric while looping through user metric
    bench_val = benchmark_metrics[metric]
    gap = bench_val - user_val

    if user_val >= bench_val * 0.8: #if you are within in 80% thats good
      rating = "good"
    elif user_val >= bench_val * 0.5: #if you are within between 50-80% thats fine
      rating = "needs improvement"
    else: #if you are significantly behind the behcnmark
      rating = "below benchmark"

    results[metric]= {
      "your_value": user_val,
      "benchmark_value":bench_val,
      "gap":round(gap,2),
      "rating":rating
    }
  return results


def extract_commit_messages(commits: list) -> list:
    return [c["commit"]["message"] for c in commits]

def extract_pr_descriptions(prs: list) -> list:
    return [pr["body"] for pr in prs if pr["body"]]

def build_composite_benchmark(all_contributor_commits: list[list]) -> dict:
    # analyze each contributor's commits
    all_metrics = [analyze_commits(commits) for commits in all_contributor_commits if commits]
    
    if not all_metrics:
        return {}
    
    # average each metric across all contributors
    keys = all_metrics[0].keys()
    composite = {}
    for key in keys:
        values = [m[key] for m in all_metrics]
        composite[key] = round(sum(values) / len(values), 2)
    
    return composite


def score_against_benchmark(user_metrics: dict, benchmark: dict) -> dict:
    if not benchmark:
        return {"total": 0.0, "breakdown": {}}
    
    breakdown = {}
    scores = []
    
    for key in benchmark:
        if benchmark[key] == 0:
            score = 100.0 if user_metrics.get(key, 0) == 0 else 50.0
        else:
            score = min(user_metrics.get(key, 0) / benchmark[key], 1.0) * 100
        
        score = round(score, 1)
        scores.append(score)
        breakdown[key] = {
            "your_value": user_metrics.get(key, 0),
            "benchmark_value": benchmark[key],
            "score": score
        }
    
    total = round(sum(scores) / len(scores), 1)
    return {"total": total, "breakdown": breakdown}



  