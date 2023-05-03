import requests
import json
import os

# improve this function to check if the user is already registered
async def findOrCreateUser(interaction):

    ## Only to find if the records exists as a participant
    x_find = requests.get(os.environ["API_URL"] + f'/guilds/' + str(interaction.guild_id) + '/participants/' + str(interaction.user.id), headers={
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
        x_create = requests.post(os.environ["API_URL"] + f'/guilds/' + str(interaction.guild_id) + '/participants/', data= json.dumps(data), headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.environ["API_KEY"]
        })

        create = x_create.json()

        return create
    
    # This line returns the JSON response
    return find


async def assignUserRole(discord_id, role_id=''):
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
