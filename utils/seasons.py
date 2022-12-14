import requests
import json
import os


async def getSeasons(discord_id:str=None, unregistered:bool=False):
    
    route=f'/options/seasons/{discord_id}?unregistered={unregistered}' if discord_id != None else '/options/seasons'
    

    x = requests.get(os.environ["API_URL"] + route, headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.environ["API_KEY"]
        })

    return x.json()

async def getRandomQuestion(season_id):
    route = f'/trivia/random-event/{season_id}'

    x = requests.get(os.environ["API_URL"] + route, headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ["API_KEY"]
    })

    return x.json()