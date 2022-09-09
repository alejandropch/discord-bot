import discord
from utils.userExists import handle as userExists
from utils.User import User
from utils.getFields import handle as getFields


async def handle(interaction: discord.Interaction, season: str, winner: User):
    winner.clear()
    exists = await userExists(str(interaction.user.id),season)
    if exists["status"]=="error":
        raise NameError(exists["message"])

    exists = await userExists(str(interaction.user.id))
    if exists is None:
        fields = getFields(season)
        if fields["status"] == "error":
            raise NameError(fields["message"])
        await winner.setRemanaingData(interaction, season, fields['data'])
        return [f"Thanks for registering - I sent you a direct message, please check settings if you did not receive it.", False]

    return [f"Hey {interaction.user.name}, seems that we tried to register you again. Buy you're already on our database!. Sorry ☹️", True]
