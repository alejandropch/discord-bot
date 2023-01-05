import discord
import requests
from dotenv import load_dotenv
import json
import os
from discord.ext import commands
from discord import app_commands
from utils.seasons import getRandomQuestion
from interactions.trivia import handle as handleTrivia

class SeasonButtons(discord.ui.View):
    def __init__(self, options = [], question = ''):
        super().__init__(timeout=180)
        self.options = options
        self.question = question
        self.build_buttons()
    
    def build_buttons(self):

        callbacks = {}
        for idx, option in enumerate(self.options):
            button = discord.ui.Button(label=option['name'], style=discord.ButtonStyle.blurple)

            button.callback = self.generate_callback(option = option)

            self.add_item(button)


    def generate_callback(self, option: str):
        
        async def validate_button(interaction: discord.Interaction):
                response = await getRandomQuestion(season_id=option['id'])
                if response['status'] == 'success':
                    if response['data']['multiple']:
                        await interaction.response.send_message(response['data']['question'], view=Buttons(options=response['data']['options'], event=response['data']['event'], question=response['data']['question']), ephemeral=True)
                    else:
                        await interaction.response.send_modal(TriviaModal(title=response['data']['question'], event=response['data']['event']))
                else:
                    await interaction.response.send_message(response['message'], ephemeral=True)
        
        return validate_button

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

class TriviaModal(discord.ui.Modal):
    def __init__(self, title = 'Trivia!', event = ''):
        super().__init__(title = title)
        self.event = event

    answer = discord.ui.TextInput(label = 'Answer', style = discord.TextStyle.short, required = True)

    async def on_submit(self, interaction: discord.Interaction):
        response = await handleTrivia(interaction, self.event, self.answer.value)
        embed = discord.Embed(title = self.title, description = f"**{self.answer.label}**\n{self.answer}\n\n**{response}**")
        embed.set_author(name = interaction.user, icon_url = interaction.user.avatar)
        await interaction.response.send_message(embed = embed, ephemeral = True)