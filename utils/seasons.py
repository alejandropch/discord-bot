import requests
import json
import os

# General Utility functions for seasons


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


async def getRandomQuestion(season_id, user):
    route = f'/trivia/random-event/{season_id}'

    x = requests.get(os.environ["API_URL"] + route, params={ 'discord_id': str(user.id)}, headers={
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

async def findOrCreateUser(interaction):

    ## Only to find if the records exists as a participant
    x_find = requests.get(os.environ["API_URL"] + f'/participants/' + str(interaction.user.id), headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ["API_KEY"]
    })
    # This line decodes the response from the request as JSON and assigns it to a variable
    find = x_find.json()
    if find['status'] != 'success':
        
        data={
            "discord_id": str(interaction.user.id),
            "discord_username": interaction.user.name + '#' + interaction.user.discriminator,
            "avatar_url": str(interaction.user.avatar.url if interaction.user.avatar is not None else '')
        }
        ## Create as a Participant
        x_create = requests.post(os.environ["API_URL"] + f'/participants/', data= json.dumps(data), headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.environ["API_KEY"]
        })

        create = x_create.json()

        return create
    
    # This line returns the JSON response
    return find

async def assignRole(discord_id, role_id=''):
    if role_id =='':
        return

    data = {
        'member': {
            'discord_id':discord_id,
            'role_id' : role_id
        },
        'guild_id': os.environ["GUILD_ID"]
    }
    x = requests.put(os.environ["API_URL"] + f'/participants/assign-role', data = json.dumps(data), headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ["API_KEY"]
    })

    res = x.json()
    if(res['status']!= "success"):
        raise Exception(res['message'])
    
    return res

def handleSuccessfulResponse(number_of_questions):
    if len(number_of_questions) > 0:
                return "Form sent successfully!"
            
    if len(number_of_questions) == 0:
        return "You have successfully registered!"