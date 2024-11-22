import aiohttp
import asyncio

base_url = "af-link.ru"

async def check_user(user_id):
    url = "https://af-link.ru/api/check/user"
    json_data = {"username": f"{user_id}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json_data) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {"status": False, "error": "Request failed"}


async def add_link(user_id, link):
    url = "https://af-link.ru/api/link/add"
    json_data = {"username": f"{user_id}", "link": link}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json_data) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {"status": False, "error": "Request failed"}


async def list_link(user_id):
    url = "https://af-link.ru/api/link/list"
    json_data = {"username": f"{user_id}"}
    
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json_data) as response:
            if response.status == 200:
                return await response.json()
            else:
                return {"status": False, "error": "Request failed"}