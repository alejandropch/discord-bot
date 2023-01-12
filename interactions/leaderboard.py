import discord
import requests
from dotenv import load_dotenv
import json
import os

async def handle(interaction: discord.Interaction, season: int):
    data = {
        "member": {
            "discord_id": str(interaction.user.id),
            "discord_username": interaction.user.name + '#' + interaction.user.discriminator,
            "avatar_url": str(interaction.user.avatar.url if interaction.user.avatar is not None else '')
        },
        "season": season
    }

    x = requests.get(os.environ["API_URL"] + '/leaderboard/' + str(season), headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.environ["API_KEY"]
        })
        
    return x.json()

async def getSeasons():
    x = requests.get(os.environ["API_URL"] + '/options/leaderboard', headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.environ["API_KEY"]
        })

    return x.json()
