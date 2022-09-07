from cmath import log
import requests
import os
from dotenv import load_dotenv
import json


async def handle(discord_id):
    """ It will return None if the user does not exists in the db """
    value = requests.get(os.environ["API_URL"] + f'/participants/{discord_id}', headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ["API_KEY"]
    })
    res = json.loads(value.text)['data']
    return res
