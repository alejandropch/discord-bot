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
from interactions.mult import handle as handleMult
from interactions.mult import getEvent
# views
from views.views import Buttons
from views.modal import TriviaModal


load_dotenv()
bot_token = os.environ["BOT_TOKEN"]


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
        if winner.isWinner == False:
            return

        [isValid, errMessage] = winner.errorHandler(message.content, True)
        user = await client.fetch_user(message.author.id)

        if isValid == False:
            await user.send(f"Value provided is invalid. {errMessage}")
        else:
            winner.nextQuestion()

        await winner.dmUser()


client = aclient()
winner = User(client)

tree = app_commands.CommandTree(client)


@ tree.command(guild=discord.Object(id=os.environ["GUILD_ID"]), name='register', description='Register an user')
async def register(interaction: discord.Interaction, season: str):
    try:
        [response, isRegistered] = await handleRegister(interaction, season, winner)
        await interaction.response.send_message(response, ephemeral=True)
        if isRegistered is True:
            return
        await winner.dmUser()
    except NameError as err:
        await interaction.response.send_message(err, ephemeral=True)


@tree.command(guild=discord.Object(id=os.environ["GUILD_ID"]), name='attendance', description='Attend discord events and earn points')
async def attendance(interaction: discord.Interaction, event: str):
    await interaction.response.send_message(f"You've selected the attendance slash command", ephemeral=True)


@tree.command(guild=discord.Object(id=os.environ["GUILD_ID"]), name='random', description='Random events to earn points')
async def random(interaction: discord.Interaction, event: str):
    response = await handleRandom(interaction, event)
    await interaction.response.send_message(response, ephemeral=True)


@tree.command(guild=discord.Object(id=os.environ["GUILD_ID"]), name='trivia', description='Answer trivia questions and earn points')
async def trivia(interaction: discord.Interaction, event: str):
    response = await getEvent(event)
    print(response)
    if response['status'] == 'success':
        if response['data']['multiple']:
            await interaction.response.send_message(response['data']['question'], view=Buttons(options=response['data']['options'], event=event, question=response['data']['question']), ephemeral=True)
        else:
            await interaction.response.send_modal(TriviaModal(title=response['data']['question'], event=event))
    else:
        await interaction.response.send_message(response['message'], ephemeral=True)



@tree.command(guild=discord.Object(id=os.environ["GUILD_ID"]), name='leaderboard', description='Season Leaderboard')
async def leaderboard(interaction: discord.Interaction, season: str):
    response = await handleLeaderboard(interaction, season)
    await interaction.response.send_message(response, ephemeral=True)

client.run(bot_token)
