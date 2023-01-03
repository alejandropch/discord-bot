import requests
import json
import os

#General Utility functions for seasons


async def getSeasons(discord_id: str = None, unregistered: bool = False):
    route = f'/options/seasons/{discord_id}?unregistered={unregistered}' if discord_id != None else '/options/seasons'

    x = requests.get(os.environ["API_URL"] + route, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ["API_KEY"]
    })

    res = x.json()

    if res['status'] != 'success':
        raise ValueError(res['message'])

    return res

# gets a random event question from the selected season

    return x.json()

#gets a random event question from the selected season
async def getRandomQuestion(season_id):
    route = f'/trivia/random-event/{season_id}'

    x = requests.get(os.environ["API_URL"] + route, headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ["API_KEY"]
    })

    return x.json()

#gets all the registration fields for the selected season
async def getFields(season_id):
    route = f'/seasons/{season_id}/fields'

    x = requests.get(os.environ["API_URL"] + route, headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ["API_KEY"]
    })

    return x.json()