import requests
import logging
import aiohttp
import os

async def make_async_request_put(url: str, headers:dict, data: dict):
    '''
    Make async http request
    '''
    #logging.info(url, headers, data)
    async with aiohttp.ClientSession() as session:
        async with session.put(url, headers=headers, json=data) as response:
            return await response.text()

async def make_async_request_post(url: str, headers:dict, data: dict):
    '''
    Make async http request
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            return await response.text()

async def get_image(prompt):
    url = 'https://discord.com/api/v9/interactions'
    auth = {
      'authorization': os.getenv("AUTH_TOKEN")
      #'authorization': "MTA5NjExMjQxMzE0Njg5NDQzNw.G40cOT.w3XybsZRmg3sXG2DpEDxThpxDr44nmmiE0tuWI"
    }
    msg = {"type":2,
    "application_id":"936929561302675456",
    "guild_id":"1094995526769987704",
    "channel_id":"1095343240594595900",
    "session_id":"4727a474a9f3f5cc4de5515003a5d3bc",
    "data":{"version":"1077969938624553050",
    "id":"938956540159881230",
    "name":"imagine",
    "type":1,
    "options":[{"type":3,
    "name":"prompt",
    "value":"asdasdasdasfasfasfasdfsdas"}],
    }}
    # msg = {"type":2,
    # "application_id":"1032699319368814652",
    # "guild_id":"1094995526769987704",
    # "channel_id":"1095343240594595900",
    # "session_id":"2e224721645708c191a4f38585994b53",
    # "data":
    # {"version":"1093695818164338708",
    # "id":"1037145598782099518",
    # "name":"generate",
    # "type":1,
    # "options":[{"type":3,
    # "name":"description",
    # "value":prompt}],
    # }}

    await make_async_request_post(url, headers = auth, data = msg)
    #requests.post(url, headers=auth, json=msg)

async def send_image(mesageid_sseed, img_url, prompt, DS_HOST='localhost'):
    url = f'http://{DS_HOST}:8000/api/ds/load_image/'
    auth = {
        'authorization': os.getenv("AUTH_TOKEN")
    }

    data = {
    "prompt": prompt,
    "mesageid_sseed": mesageid_sseed,
    "image_url": img_url
    }
    await make_async_request_put(url, headers=auth, data=data)
    #requests.put(url, headers=auth, json=data)
