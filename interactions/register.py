import discord
from utils.userExists import handle as userExists
from utils.User import User
from utils.getFields import handle as getFields


async def handle(interaction: discord.Interaction, season: str, participant: User):
    participant.clear()
    exists = await userExists(str(interaction.user.id),season)
    if exists["status"]=="error":
        raise NameError(exists["message"])


        
    fields = getFields(season)
    if fields["status"] == "error":
        raise NameError(fields["message"])
    await participant.setRemanaingData(interaction, season, fields['data'])
    if participant.nQuestions == 0:    
        try:
            await participant.handleRequest(participant)
            return ["Thanks for registering!",True]
        except:
            return ["Something has broken, we are fixing it!!",True]
    return [f"Thanks for registering - I sent you a direct message, please check settings if you did not receive it.", False]

