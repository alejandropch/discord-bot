import discord
import requests
from dotenv import load_dotenv
import json
import os
from discord.ext import commands
from discord import app_commands
#install discord.py newest version with: python3 -m pip install -U git+https://github.com/Rapptz/discord.py

from interactions.trivia import handle as handleTrivia
from interactions.random import handle as handleRandom

load_dotenv()
bot_token = os.environ["BOT_TOKEN"]

class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Click me!",style=discord.ButtonStyle.red)
    async def blue_button(self,button:discord.ui.Button,interaction:discord.Interaction):
        await interaction.response.edit_message(content=f"You clicked the button!!")

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild = discord.Object(id = os.environ["GUILD_ID"]))
            self.synced = True
        print(f"We have logged in as {self.user}.")

client = aclient()
tree = app_commands.CommandTree(client)

@tree.command(guild = discord.Object(id = os.environ["GUILD_ID"]), name = 'trivia', description = 'Answer trivia questions and earn points')
async def trivia(interaction: discord.Interaction, event: str, answer: str):
    response = await handleTrivia(interaction, event, answer)
    await interaction.response.send_message(response, ephemeral = True)

@tree.command(guild = discord.Object(id = os.environ["GUILD_ID"]), name = 'attendance', description = 'Attend discord events and earn points')
async def attendance(interaction: discord.Interaction, event: str):
    await interaction.response.send_message(f"You've selected the attendance slash command", ephemeral = True)

@tree.command(guild = discord.Object(id = os.environ["GUILD_ID"]), name = 'random', description = 'Random events to earn points')
async def random(interaction: discord.Interaction, event: str):
    response = await handleRandom(interaction, event)
    await interaction.response.send_message(response, ephemeral = True)

@tree.command(guild = discord.Object(id = os.environ["GUILD_ID"]), name = 'button', description = 'Shows test button')
async def button(interaction: discord.Interaction):
    await interaction.response.send_message(f"Register by clicking the button", view = Buttons(), ephemeral = True)

client.run(bot_token)