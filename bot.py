import discord
import requests
from dotenv import load_dotenv
import json
import os

load_dotenv()
bot_token = os.environ["BOT_TOKEN"]

intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Connected as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        participant = {
            'id': str(message.author.id),
            'avatar_url': message.author.avatar_url,
            'name': message.author.name,
            'display_name': message.author.display_name,
            'discriminator': message.author.discriminator,
            'joined_at': message.author.joined_at,
        }

        req = requests.post(os.environ["API_URL"] + '/api/participant', data = json.dumps(participant), headers = {
            'Content-Type': 'aplication/json'
        })


client.run(bot_token)