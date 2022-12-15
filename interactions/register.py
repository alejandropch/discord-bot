import discord
from utils.userExists import handle as userExists
from utils.User import User
from utils.getFields import handle as getFields


async def handle(interaction: discord.Interaction, season_id: str, participant: User):
    participant.clear()
    exists = await userExists(interaction,season_id)

    if exists["status"]=="error":
        raise NameError(exists["message"])


        
    fields = getFields(season_id)
    if fields["status"] == "error":
        raise NameError(fields["message"])
    await participant.setRemainingData(interaction, season_id, fields['data']) 
    if participant.nQuestions == 0:    
        try:
            await participant.handleRequest(participant)
            return ["Thanks for registering!",True]
        except:
            return ["Something has broken, we are fixing it!!",True]
    return [f"Thanks for registering - I sent you a direct message, please check settings if you did not receive it.", False]

