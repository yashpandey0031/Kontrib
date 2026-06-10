import httpx
import asyncio

async def check_rate_limit():
    headers = {"Authorization": f"Bearer YOUR_TOKEN"}
    async with httpx.AsyncClient() as client:
        r = await client.get("https://api.github.com/rate_limit", headers=headers)
        print(r.json())

asyncio.run(check_rate_limit())