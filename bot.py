from pickle import FALSE
from tabnanny import check
from urllib import response
import discord
from dotenv import load_dotenv
import os
from discord.ext import commands
from discord import app_commands

from utils.User import User
from utils.seasons import getSeasons
from utils.userExists import handle as userExists

# install discord.py newest version with: python3 -m pip install -U git+https://github.com/Rapptz/discord.py

from interactions.trivia import handle as handleTrivia
from interactions.random import handle as handleRandom
from interactions.leaderboard import handle as handleLeaderboard
#from interactions.leaderboard import getSeasons
from interactions.mult import handle as handleMult
from interactions.mult import getEvent
from views.registration import RegisterModal as RegisterOneSeasonModal

# views
from views.views import Buttons
from views.trivia import SeasonButtons as TriviaSeasonButtons
from views.registration import RegisterButtons as RegisterSeasonButtons

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


client = aclient()
tree = app_commands.CommandTree(client)


@tree.command(guild=discord.Object(id=os.environ["GUILD_ID"]), name='register', description='Register an user')
async def register(interaction: discord.Interaction):
    participant = User(client)
    # registering the user into the db if not already

    is_register = await userExists(interaction)

    if is_register['status'] != 'success':
        await interaction.response.send_message(is_register['message'], ephemeral=True)

    response = await getSeasons(discord_id=str(interaction.user.id), unregistered=True)

    if response['status'] != 'success':
        await interaction.response.send_message(response['message'], ephemeral=True)

    # if there is no seasons
    if len(response['data']['options']) == 0:
        await interaction.response.send_message("Seems that there are not any seasons available to register", ephemeral=True)
    # if there is one season
    elif len(response['data']['options']) == 1:
        season_id = response['data']['options'][0]['id']
        await handleRegister(interaction, season_id, participant)
        await interaction.response.send_modal(RegisterModal(participant=participant, one_season=True))
    else:
        # if there is more than one season
        await interaction.response.send_message(response['data']['question'], view=RegisterSeasonButtons(options=response['data']['options'], question=response['data']['question'], participant=participant), ephemeral=True)


@tree.command(guild=discord.Object(id=os.environ["GUILD_ID"]), name='attendance', description='Attend discord events and earn points')
async def attendance(interaction: discord.Interaction, event: str):
    await interaction.response.send_message(f"You've selected the attendance slash command", ephemeral=True)


@tree.command(guild=discord.Object(id=os.environ["GUILD_ID"]), name='random', description='Random events to earn points')
async def random(interaction: discord.Interaction, event: str):
    response = await handleRandom(interaction, event)
    await interaction.response.send_message(response, ephemeral=True)


@tree.command(guild=discord.Object(id=os.environ["GUILD_ID"]), name='trivia', description='Answer trivia questions and earn points')
async def trivia(interaction: discord.Interaction):
    response = await getSeasons(discord_id=str(interaction.user.id))
    if response['status'] == 'success':
        await interaction.response.send_message(response['data']['question'], view=TriviaSeasonButtons(options=response['data']['options'], question=response['data']['question']), ephemeral=True)
    else:
        await interaction.response.send_message(response['message'], ephemeral=True)


@tree.command(guild=discord.Object(id=os.environ["GUILD_ID"]), name='leaderboard', description='Season Leaderboard')
async def leaderboard(interaction: discord.Interaction):
    response = await getSeasons()
    if response['status'] == 'success':
        await interaction.response.send_message(response['data']['question'], view=SeasonButtons(options=response['data']['options'], question=response['data']['question']), ephemeral=True)
    else:
        await interaction.response.send_message(response['message'], ephemeral=True)


client.run(bot_token)
