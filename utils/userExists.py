from cmath import log
import requests
import os
from dotenv import load_dotenv
import json


async def handle(discord_id, season:str):
    """ It will return None if the user does not exists in the db """
    data={
        "season":season,
        "member":{
            "discord_id":discord_id
        }
    }
    value = requests.post(os.environ["API_URL"] + f'/participants/check', data=json.dumps(data), headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ["API_KEY"]
    })

    res = json.loads(value.text)
    return res
