#test script for checking if it is actually calling the API 

import asyncio
import json
from github_client import get_user, get_user_commits, get_top_contributors,get_user_prs
from analyzer import analyze_commits, extract_commit_messages
from llm_client import analyze_with_llm
from analyzer import extract_commit_messages,compare



async def main():
  # user = await get_user("yashpandey0031")
  # print(user["name"], user["public_repos"])
  
  top = await get_top_contributors("microsoft/vscode",limit = 3)
  print([c['login'] for c in top])

  #test fetching commits, from the top of vs code commitor
  commits = await get_user_commits(top[0]['login'], "microsoft/vscode")
  print(f"Top contributors: {[c['login'] for c in top]}")
  bench_result = analyze_commits(commits)
  print(bench_result)

  #fetch your own commits for comparing against the above top benchmark values
  your_commits = await get_user_commits("yashpandey0031", "yashpandey0031/coral-reefs-nlp")
  your_result = analyze_commits(your_commits)
  print(your_result)

  messages = extract_commit_messages(your_commits)
  print(messages)

  benchmark_messages = extract_commit_messages(commits)
  comparison = compare(your_result,bench_result)
  

  result = analyze_with_llm(
    username="yashpandey0031",
    user_messages=messages,
    benchmark_username=top[0]['login'],
    benchmark_messages=benchmark_messages,
    metrics_comparison=comparison
    )   
  
  print(result)

   
  # print(json.dumps(comparison,indent=2))

  

  #test fetching the top contributors, from a main repo 
  # top = await get_top_contributors("facebook/react", limit=3)
  # print(f"Top contributors: {[c['login'] for c in top]}")

  #anayze commits
  

  # commits = await get_user_commits("torvalds", "torvalds/linux")
  # print(json.dumps(commits[0], indent=2)) #print everything related to that dude here 

asyncio.run(main())


