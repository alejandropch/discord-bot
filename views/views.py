import discord
import requests
from dotenv import load_dotenv
import json
import os
from discord.ext import commands
from discord import app_commands
from interactions.trivia import handle as handleTrivia
from interactions.leaderboard import handle as handleLeaderboard
from utils.User import User
from utils.seasons import getFields

class Buttons(discord.ui.View):
    def __init__(self, options = [], event = '', question = ''):
        super().__init__(timeout=180)
        self.options = options
        self.event = event
        self.question = question
        self.build_buttons()
    
    def build_buttons(self):

        callbacks = {}
        for idx, option in enumerate(self.options):
            button = discord.ui.Button(label=option, style=discord.ButtonStyle.blurple)

            button.callback = self.generate_callback(option = option)

            self.add_item(button)


    def generate_callback(self, option: str):
        
        async def validate_button(interaction: discord.Interaction):
                response = await handleTrivia(interaction, self.event, option)
                embed = discord.Embed(title = self.question, description = f"**Answer**\n{option}\n\n**{response}**")
                embed.set_author(name = interaction.user, icon_url = interaction.user.avatar)
                await interaction.response.edit_message(embed = embed, content = None, view = None)
        
        return validate_button

class RegisterButtons(discord.ui.View):
    def __init__(self, options = [], question = '', participant:User=None):
        super().__init__(timeout=180)
        self.options = options
        self.question = question
        self.build_buttons()
        self.participant = participant
    
    def build_buttons(self):

        callbacks = {}
        for idx, option in enumerate(self.options):
            button = discord.ui.Button(label=option['name'], style=discord.ButtonStyle.blurple)

            button.callback = self.generate_callback(option = option)

            self.add_item(button)


    def generate_callback(self, option: str):
        
        async def validate_button(interaction: discord.Interaction):
            response = await getFields(season_id=option['id'])
            await interaction.response.send_modal(RegisterModal(participant=participant,one_season=True))
        
        return validate_button

