from cmath import log
import requests
import os
from dotenv import load_dotenv
import json


async def handle(discord_id):

    value = requests.get(os.environ["API_URL"] + f'/participants/{discord_id}', headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ["API_KEY"]
    })
    res = json.loads(value.text)['data']
    return res
