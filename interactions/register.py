import discord
from cmath import log
import requests
import os
import json
from dotenv import load_dotenv
from utils.userExists import handle as userExists


async def handle(user):
    print(user.discordUsername)
    data = {
        "member": {
            "name": user.name,
            "lastname": user.lastName,
            "address_1": user.address1,
            "address_2": user.address2,
            "city": user.city,
            "state": user.state,
            "postal_code": user.postalCode,
            "country": user.country,
            "discord_id": user.discord_id,
            "discord_username": user.discordUsername,
            "avatar_url": user.avatar_url,
            "winner": user.isWinner
        },
    }

    value = requests.post(os.environ["API_URL"] + '/participants/', data=json.dumps(data), headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ["API_KEY"]
    })
    print(value.json())

    try:
        value.json()
        print(value.text)
    except json.decoder.JSONDecodeError:
        print("json empty")

    return
