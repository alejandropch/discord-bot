import discord
import requests
from dotenv import load_dotenv
import json
import os

async def handle(discord_id:int, season:int):

    x = requests.get(os.environ["API_URL"] + '/leaderboard/' + str(discord_id) + "/season/" + str(season), headers = {
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
