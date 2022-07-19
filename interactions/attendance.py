import discord
import requests
from dotenv import load_dotenv
import json
import os

async def handle(interaction: discord.Interaction, event: str):
    data = {
        "member": {
            "discord_id": str(interaction.user.id),
            "discord_username": interaction.user.name + '#' + interaction.user.discriminator,
            "avatar_url": str(interaction.user.avatar.url if interaction.user.avatar is not None else '')
        },
        "event_code": event,
    }

    x = requests.post(os.environ["API_URL"] + '/interactions/attendance', data = json.dumps(data), headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.environ["API_KEY"]
        })
        
    return x.json()['message']

