import asyncio
from github_client import get_user

async def main():
  user = await get_user("yashpandey0031")
  print(user["name"], user["public_repos"])

asyncio.run(main())