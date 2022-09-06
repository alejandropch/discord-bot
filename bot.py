from pickle import FALSE
from tabnanny import check
from urllib import response
import discord
from dotenv import load_dotenv
import os
from discord.ext import commands
from discord import app_commands

#from ui.YorNButtons import YorNButtons
from utils.User import User
from utils.userExists import handle as userExists

# install discord.py newest version with: python3 -m pip install -U git+https://github.com/Rapptz/discord.py

from interactions.register import handle as handleForm
from interactions.trivia import handle as handleTrivia
from interactions.random import handle as handleRandom
from interactions.leaderboard import handle as handleLeaderboard
from utils.formErrorHandler import checkIfError, formErrorHandler

load_dotenv()
bot_token = os.environ["BOT_TOKEN"]
i = 0


class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.red)
    async def blue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content=f"You clicked the button!!")


class YorNButtons(discord.ui.View):
    def __init__(self, *, timeout=None):
        super().__init__(timeout=timeout)
        self.value = None

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, custom_id="yes")
    async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        if self.value == None:
            try:
                await handleForm(winner)
                await interaction.response.send_message(content="Form sent successfully!")
                self.value = True
            except:
                await interaction.response.send_message(content='Something has broken, we are fixing it!')
            return

        else:
            await interaction.response.edit_message(content=f"You already clicked this button!!")
        return

    @discord.ui.button(label="No", style=discord.ButtonStyle.red, custom_id="no")
    async def no_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        global i

        if self.value == None:
            # the user wants to restart the form summision
            await interaction.response.send_message(content=f"let's start again")
            winner.clear()
            self.value = False
            i = 0
            user = await client.fetch_user(str(interaction.user.id))
            return await dmUser(user)
        else:
            await interaction.response.edit_message(content=f"You already clicked this button!!")
        return

    def getValue(self):
        return self.value


async def dmUser(user, isValid=True, msg=""):
    global i

    def check(message):
        return False if checkIfError(message.content) is False else True

    if i == 0:
        await user.send("What is your first name?")

        name = (await client.wait_for("message", check=check)).content
        if name == "":
            return

        winner.name = isValid and name or ''

    if i == 1:
        await user.send("What is your last name?")
        lastName = (await client.wait_for("message", check=check)).content
        if lastName == "":
            return
        winner.lastName = isValid and lastName or ''

    if i == 2:
        await user.send("Please provide your Address (first line)")
        address1 = (await client.wait_for("message", check=check)).content
        if address1 == "":
            return
        winner.address1 = isValid and address1 or ''

    if i == 3:
        await user.send("Please provide your Address 2 (if none, please type '-')")
        address2 = (await client.wait_for("message", check=check)).content

        if address2 == "" or address2.strip() == "-":

            return
        winner.address2 = isValid and address2 or ''

    if i == 4:
        await user.send("Please provide your City")
        city = (await client.wait_for("message", check=check)).content
        if city == "":
            return
        winner.city = isValid and city or ''

    if i == 5:
        await user.send("Please provide your State/Province")
        state = (await client.wait_for("message", check=check)).content
        if state == "":
            return

        winner.state = isValid and state or ''

    if i == 6:
        await user.send("Please provide your Postal Code")
        postalCode = (await client.wait_for("message", check=check)).content
        if postalCode == "":
            return
        winner.postalCode = isValid and postalCode or ''

    if i == 7:
        await user.send("Please provide your Country")
        country = (await client.wait_for("message", check=check)).content
        if country == "":
            return
        winner.country = isValid and country or ''

    if i == 8:
        # filling the remaining data from discord to the CE admin
        view = YorNButtons()
        winner.setRemanaingData(user)
        await winner.printResult(user)
        await user.send('Does this look correct?\nClick **\"Yes\"** to submit \nClick **\"No\"** for start over', view=view)


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=os.environ["GUILD_ID"]))
            self.synced = True
        print(f"We have logged in as {self.user}.")

        # TODO: make a trigger from admin
        # await dmUser(self)

    async def on_message(self, message):
        global i
        if message.author == self.user:
            """ print(message) """
            return

        # the form have already been printed
        [isValid, message] = formErrorHandler(message.content)

        if isValid == True:
            i += 1
            """ await dmUser(self, isValid=True) """

        else:
            """ return await dmUser(self, isValid, message) """


client = aclient()
winner = User()

tree = app_commands.CommandTree(client)


@ tree.command(guild=discord.Object(id=os.environ["GUILD_ID"]), name='trivia', description='Answer trivia questions and earn points')
async def trivia(interaction: discord.Interaction, event: str, answer: str):
    response = await handleTrivia(interaction, event, answer)
    await interaction.response.send_message(response, ephemeral=True)


@tree.command(guild=discord.Object(id=os.environ["GUILD_ID"]), name='attendance', description='Attend discord events and earn points')
async def attendance(interaction: discord.Interaction, event: str):
    await interaction.response.send_message(f"You've selected the attendance slash command", ephemeral=True)


@ tree.command(guild=discord.Object(id=os.environ["GUILD_ID"]), name='random', description='Random events to earn points')
async def random(interaction: discord.Interaction, event: str):
    response = await handleRandom(interaction, event)
    await interaction.response.send_message(response, ephemeral=True)


@ tree.command(guild=discord.Object(id=os.environ["GUILD_ID"]), name='button', description='Shows test button')
async def button(interaction: discord.Interaction):
    await interaction.response.send_message(f"Register by clicking the button", view=Buttons(), ephemeral=True)


@tree.command(guild=discord.Object(id=os.environ["GUILD_ID"]), name='leaderboard', description='Season Leaderboard')
async def leaderboard(interaction: discord.Interaction, season: str):
    response = await handleLeaderboard(interaction, season)
    await interaction.response.send_message(response, ephemeral=True)

client.run(bot_token)
