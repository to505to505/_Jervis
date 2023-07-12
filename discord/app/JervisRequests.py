import requests
import logging
import aiohttp
import os

auth = {
    'authorization': os.getenv("AUTH_TOKEN")
    #'authorization': "MTA5NjExMjQxMzE0Njg5NDQzNw.G40cOT.w3XybsZRmg3sXG2DpEDxThpxDr44nmmiE0tuWI"
}

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

async def fast_mode():
    url = 'https://discord.com/api/v9/interactions'
    msg = {"type":2,
     "application_id":"936929561302675456",
     "guild_id":"1094995526769987704",
     "channel_id":"1095343240594595900",
     "session_id":"13f67e33816ae28205bc4c032cf12296",
     "data":{"version":"987795926183731231",
             "id":"972289487818334212",
             "name":"fast",
             "type":1,
             "options":[],
             "application_command":{"id":"972289487818334212",
                                    "application_id":"936929561302675456",
                                    "version":"987795926183731231",
                                    "default_member_permissions":"null",
                                    "type":1,
                                    "nsfw":"false",
                                    "name":"fast"},
             "attachments":[]}}
    await make_async_request_post(url, headers = auth, data = msg)    
    #requests.post(url, headers=auth, json=msg)

async def relax_mode():
    url = 'https://discord.com/api/v9/interactions'
    msg = {"type":2,
     "application_id":"936929561302675456",
     "guild_id":"1094995526769987704",
     "channel_id":"1095343240594595900",
     "session_id":"13f67e33816ae28205bc4c032cf12296",
     "data":{"version":"987795926183731231",
             "id":"972289487818334212",
             "name":"fast",
             "type":1,
             "options":[],
             "application_command":{"id":"972289487818334212",
                                    "application_id":"936929561302675456",
                                    "version":"987795926183731231",
                                    "default_member_permissions":"null",
                                    "type":1,
                                    "nsfw":"false",
                                    "name":"relax"},
             "attachments":[]}}
    await make_async_request_post(url, headers = auth, data = msg)    
    #requests.post(url, headers=auth, json=msg)

async def Im_honestly_midjourney():
    url = 'https://discord.com/api/v9/channels/1095343240594595900/messages'
    msg = {"content":"AI robot drawing a paintings - @jervis (fast)",
    "channel_id":"1095343240594595900",
    "type":0,
    "sticker_ids":[],
    "attachments":[{"id":"0",
    "filename":"jervis_Happy_cat_meow_a57531ca-fddd-4084-a6e9-80c146871c6c.png",
    "uploaded_filename":"c7515530-0982-45f9-8b19-52bc07d1b769/jervis_Happy_cat_meow_a57531ca-fddd-4084-a6e9-80c146871c6c.png"}]}
    await make_async_request_post(url, headers = auth, data = msg)
    #requests.post(url, headers=auth, json=msg)

async def get_image(prompt):
    url = 'https://discord.com/api/v9/interactions'
    msg = {"type":2,
        "application_id":"936929561302675456",
        "guild_id":"1094995526769987704",
        "channel_id":"1095343240594595900",
        "session_id":"4727a474a9f3f5cc4de5515003a5d3bc",
        "data":{"id":"938956540159881230",
        "name":"imagine",
        "type":1,
        "options":[{"type":3,
        "name":"prompt",
        "value":prompt}],
    }}
    await make_async_request_post(url, headers = auth, data = msg)
    #requests.post(url, headers=auth, json=msg)

async def send_image(mesageid_sseed, img_url, prompt, DS_HOST='localhost'):
    url = f'http://{DS_HOST}:8000/api/ds/load_image/'
    data = {
    "prompt": prompt,
    "mesageid_sseed": mesageid_sseed,
    "image_url": img_url
    }
    await make_async_request_put(url, headers=auth, data=data)
    #requests.put(url, headers=auth, json=data)

async def push_button_request(method, image_number, messageid_sseed):
    message_id, sseed = messageid_sseed.split("_")
    sseed = sseed.replace(".png", "")
    url = 'https://discord.com/api/v9/interactions'
    solo = ""
    if method == "reroll":
        solo = "::SOLO"
    #url = 'https://discord.com/api/v9/channels/1095343240594595900/messages'
    # msg = {"type":3,
    # "guild_id":"1094995526769987704",
    # "channel_id":"1095343240594595900",
    # "message_flags":0,
    # "message_id": message_id,
    # "application_id":"936929561302675456",
    # "session_id":"6df8551052ee24978d914dac28e0406c",
    # "data":{"component_type":2,
    # "custom_id":f"MJ::JOB::{method}::{image_number}::{sseed}"}}
    msg = {"type":3,
        "guild_id":"1094995526769987704",
        "channel_id":"1095343240594595900",
        "message_flags":0,
        "message_id": message_id,
        "application_id":"936929561302675456",
        "session_id":"966ba3599b3b18ee4fcf36dd62229bd6",
        "data":{"component_type":2,
        "custom_id":f"MJ::JOB::{method}::{image_number}::{sseed}{solo}"}
    }
    #msg = {"content":f"{message_id}  MJ::JOB::{method}::{image_number}::{sseed}","tts":'false',"flags":0}
    logging.info("Sending pushbutton_ask to discord!")
    await make_async_request_post(url, headers = auth, data = msg)
    #requests.post(url, headers=auth, json=msg)
