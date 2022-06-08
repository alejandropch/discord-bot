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


client.run(bot_token)