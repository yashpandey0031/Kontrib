#test script for checking if it is actually calling the API 

import asyncio
from github_client import get_user, get_user_commits, get_top_contributors

async def main():
  user = await get_user("yashpandey0031")
  print(user["name"], user["public_repos"])
  

  #test fetching commits
  commits = await get_user_commits("yashpandey0031","yashpandey0031/coral-reefs-nlp")
  print(f"Your commits in this reop: {len(commits)}")

  #test fetching the top contributors
  top = await get_top_contributors("facebook/react", limit=3)
  print(f"Top contributors: {[c['login'] for c in top]}")

asyncio.run(main())