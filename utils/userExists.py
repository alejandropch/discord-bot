from cmath import log
import requests
import os
from dotenv import load_dotenv
import json


async def handle(discord_id, season:str):
    """ This function will return None if the user does not exists in the db """
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
    # This line decodes the response from the request as JSON and assigns it to a variable
    res = json.loads(value.text)

    # This line returns the JSON response
    return res
