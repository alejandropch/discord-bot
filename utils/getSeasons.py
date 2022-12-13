import requests
import json
import os


async def handle(discord_id:str=None):
    
    route=f'/options/seasons/{discord_id}' if discord_id != None else '/options/seasons'
    

    x = requests.get(os.environ["API_URL"] + route, headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.environ["API_KEY"]
        })

    return x.json()