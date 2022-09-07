from pickle import FALSE
from tabnanny import check
from urllib import response
import discord
from dotenv import load_dotenv
import os
from discord.ext import commands
from discord import app_commands

from utils.User import User

# install discord.py newest version with: python3 -m pip install -U git+https://github.com/Rapptz/discord.py

from interactions.register import handle as handleRegister
from interactions.trivia import handle as handleTrivia
from interactions.random import handle as handleRandom
from interactions.leaderboard import handle as handleLeaderboard
from utils.formErrorHandler import formErrorHandler

load_dotenv()
bot_token = os.environ["BOT_TOKEN"]


class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)

    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.red)
    async def blue_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content=f"You clicked the button!!")


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

    async def on_message(self, message):

        if message.author == self.user:
            return

        [isValid, errMessage] = formErrorHandler(message.content)
        user = await client.fetch_user(message.author.id)

        if isValid == False:
            await user.send(f"Value provided is invalid. {errMessage}")
        else:
            winner.nextQuestion()

        # TODO: adding a condition when sending the user form
        await dmUser(user)


client = aclient()
winner = User()

tree = app_commands.CommandTree(client)


@ tree.command(guild=discord.Object(id=os.environ["GUILD_ID"]), name='register', description='Register an user')
async def register(interaction: discord.Interaction, season: str):
    # true if the user exists in the db
    isRegistered = await userExists(str(interaction.user.id))
    if isRegistered is True:
        await interaction.response.send_message(f"Hey {interaction.user.name}, seems that we tried to register you again. Buy you're already on our database!. Sorry ☹️", ephemeral=True)
        return

    # filling the remaining data from discord that must be sent to the CE admin
    winner.setRemanaingData(interaction, season)
    user = await client.fetch_user(str(interaction.user.id))
    await interaction.response.send_message(f"Thanks for registering - I sent you a direct message, please check settings if you did not receive it.", ephemeral=True)

    await dmUser(user)


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
