import discord
import requests
from dotenv import load_dotenv
import json
import os

async def handle(interaction: discord.Interaction, event: str, answer: str):
    data = {
        "member": {
            "discord_id": str(interaction.user.id),
            "discord_username": interaction.user.name + '#' + interaction.user.discriminator,
            "avatar_url": str(interaction.user.avatar.url if interaction.user.avatar is not None else '')
        },
        "event_code": event,
    }

    x = requests.post(os.environ["API_URL"] + '/interactions/trivia', data = json.dumps(data), headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.environ["API_KEY"]
        })
        
    return x.json()['message']

async def getEvent(event: str):
    x = requests.get(os.environ["API_URL"] + '/options/trivia/' + event, headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.environ["API_KEY"]
        })

    return x.json()['data']