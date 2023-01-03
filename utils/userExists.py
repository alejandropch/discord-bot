from cmath import log
import requests
import os
from dotenv import load_dotenv
import json


async def handle(interaction, season_id:str=None):
    """ This function will return None if the user does not exists in the db """
    data={
        "season_id":season_id,
        "member":{
            "discord_id": str(interaction.user.id),
            "discord_username": interaction.user.name + '#' + interaction.user.discriminator,
            "avatar_url": str(interaction.user.avatar.url if interaction.user.avatar is not None else '')
        }
    }
    value = requests.post(os.environ["API_URL"] + f'/participants/check/', data=json.dumps(data), headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ["API_KEY"]
    })
    # This line decodes the response from the request as JSON and assigns it to a variable
    res = json.loads(value.text)
    if res['status'] != 'success':
        raise ValueError (res['message'])
    # This line returns the JSON response
    return res
