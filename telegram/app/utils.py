import aiohttp
import asyncio

async def make_async_request_post(url: str, data: dict):
    '''
    Make async http request
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as response:
            return await response.text()