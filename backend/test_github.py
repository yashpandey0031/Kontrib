#test script for checking if it is actually calling the API 

import asyncio
import json
from github_client import get_user, get_user_commits, get_top_contributors
from analyzer import analyze_commits



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

  your_commits = await get_user_commits("yashpandey0031", "yashpandey0031/coral-reefs-nlp")
  your_result = analyze_commits(your_commits)
  print(your_result)

  
  

  #test fetching the top contributors, from a main repo 
  # top = await get_top_contributors("facebook/react", limit=3)
  # print(f"Top contributors: {[c['login'] for c in top]}")

  #anayze commits
  

  # commits = await get_user_commits("torvalds", "torvalds/linux")
  # print(json.dumps(commits[0], indent=2)) #print everything related to that dude here 

asyncio.run(main())


