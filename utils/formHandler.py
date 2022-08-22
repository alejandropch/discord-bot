from cmath import log
import requests
import os
import json
from dotenv import load_dotenv


async def handle(user):
    data = {
        "member": {
            "name": user.name,
            "lastname": user.lastName,
            "address_1": user.address1,
            "address_2": user.address2,
            "city": user.city,
            "state": user.state,
            "postal_code": user.postalCode,
            "country": user.postalCode,
            "discord_id": user.id,
            "discord_username": user.discordUsername,
            "winner": user.isWinner
        },
    }
    print(json.dumps(data))
    value = requests.post(os.environ["API_URL"] + '/participants/', data=json.dumps(data), headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ["API_KEY"]
    })
    try:
        value.json()
        print(value.text)
    except json.decoder.JSONDecodeError:
        print("json empty")

    return
