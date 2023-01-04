from cmath import log
import requests
import os
from dotenv import load_dotenv
import json


async def handle(interaction):

    ## Only to find if the records exists as a participant
    x_find = requests.get(os.environ["API_URL"] + f'/participants/' + str(interaction.user.id), headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + os.environ["API_KEY"]
    })
    # This line decodes the response from the request as JSON and assigns it to a variable
    find = json.loads(x_find.text)
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

        create = json.loads(x_create.text)
        print(create)

        return create
    
    # This line returns the JSON response
    return find
