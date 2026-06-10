import httpx
import os
from dotenv import load_dotenv

load_dotenv()



GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
BASE_URL = "https://api.github.com"

headers = {
  "Authorization":f"Bearer{GITHUB_TOKEN}",
  "Accept" : "application/vnd.github+json"
}



async def get_user(username: str) -> dict:
  async with httpx.AsyncClient(timeout=30.0,follow_redirects=True) as client:
    response = await client.get(f"{BASE_URL}/users/{username}", headers=headers)
    response.raise_for_status()
    return response.json()
  
async def get_user_commits(username: str, repo: str) -> list:
 
  async with httpx.AsyncClient(timeout=30.0,follow_redirects=True) as client:
    response = await client.get(
      f"{BASE_URL}/repos/{repo}/commits",
      headers = headers, 
      params={"author":username,"per_page":100}
    )
    if response.status_code in [500,422]:
      return[]
    
    response.raise_for_status()
    return response.json()
  
async def get_top_contributors(repo:  str, limit: int = 5)-> list:
  
  async with httpx.AsyncClient(timeout=30.0,follow_redirects=True) as client:
    response = await client.get(
      f"{BASE_URL}/repos/{repo}/contributors",
      headers= headers,
      params = {"per_page":limit}
    )
    if response.status_code in [500, 422]:
            return []

    response.raise_for_status()
    return response.json()
  
async def get_user_prs(username: str, repo: str) -> list:
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{BASE_URL}/repos/{repo}/pulls",
            headers=headers,
            params={
                "state": "closed",
                "per_page": 20
            }
        )
        if response.status_code in [500, 422]:
            return []
        response.raise_for_status()
        # filter only PRs by this user
        prs = response.json()
        return [pr for pr in prs if pr["user"]["login"] == username]
  