from cmath import log
import requests
import os
from dotenv import load_dotenv
import json


async def handle(interaction):
    data={
        "discord_id": str(interaction.user.id),
        "discord_username": interaction.user.name + '#' + interaction.user.discriminator,
        "avatar_url": str(interaction.user.avatar.url if interaction.user.avatar is not None else '')
    }

    ## Only to find if the records exists as a participant
    value = requests.get(os.environ["API_URL"] + f'/participants/' + str(interaction.user.id), headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ["API_KEY"]
    })
    # This line decodes the response from the request as JSON and assigns it to a variable
    res = json.loads(value.text)
    if res['status'] != 'success':
        ## Create as a Participant
        value = requests.post(os.environ["API_URL"] + f'/participants/', data, headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.environ["API_KEY"]
        })
        res = json.loads(value.text)
    # This line returns the JSON response
    return res
