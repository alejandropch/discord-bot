import discord
import requests
from dotenv import load_dotenv
import json
import os

async def handle(interaction: discord.Interaction, event: str, answer: str):
    data = {
        "member": {
            "discord_id": str(interaction.user.id),
            "discord_username": interaction.user.name,
            "avatar_url": str(interaction.user.avatar.url)
        },
        "event_code": event,
        "answer": answer
    }

    x = requests.post(os.environ["API_URL"] + '/interactions/trivia', data = json.dumps(data), headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.environ["API_KEY"]
        })
    
    return x.json()['message']

