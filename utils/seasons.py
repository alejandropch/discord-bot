import requests
import json
import os

# General Utility functions for seasons

async def get_seasons(guild_id: str = None):
    route = f'/guilds/{guild_id}/seasons'

    x = requests.get(os.environ["API_URL"] + route, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ["API_KEY"]
    })

    return x.json()


async def get_participant_seasons(guild_id: str = None, participant_id: str = None):
    route = f'/guilds/{guild_id}/participants/{participant_id}/seasons'

    x = requests.get(os.environ["API_URL"] + route, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ["API_KEY"]
    })

    return x.json()

# gets all the seasons for the selected guild 
async def get_unregistered_participant_seasons(guild_id: str = None, participant_id: str = None):
    route = f'/guilds/{guild_id}/participants/{participant_id}/seasons/not-registered'

    x = requests.get(os.environ["API_URL"] + route, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ["API_KEY"]
    })

    return x.json()

# gets a random event question from the selected season


async def getRandomQuestion(season_id, user, puzzle=False):
    route = f'/trivia/random-event/{season_id}'

    x = requests.get(os.environ["API_URL"] + route, params={ 'discord_id': str(user.id), 'puzzle': bool(puzzle)}, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ["API_KEY"]
    })

    return x.json()

# gets all the registration fields for the selected season


async def getFields(season_id):
    route = f'/seasons/{season_id}/fields'

    x = requests.get(os.environ["API_URL"] + route, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ["API_KEY"]
    })

    return x.json()



def handleSuccessfulResponse(number_of_questions):
    if len(number_of_questions) > 0:
                return "Form sent successfully!"
            
    if len(number_of_questions) == 0:
        return "You have successfully registered!"