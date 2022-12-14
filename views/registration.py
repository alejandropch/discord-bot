import discord
import requests
from dotenv import load_dotenv
import json
import os
from discord.ext import commands
from discord import app_commands
from utils import User
from utils.seasons import getRandomQuestion
from utils.seasons import getFields

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
            await interaction.response.send_modal(RegistrationModal(fields=response['data']))
        
        return validate_button

class RegistrationModal(discord.ui.Modal):
    def __init__(self, title = 'Trivia!', fields = []):
        super().__init__(title = title)
        self.fields = fields
        self.build()

    def build(self):
        for field in self.fields:
            text_input = discord.ui.TextInput(label = field['question'], style = discord.TextStyle.short,required = True)
            self.add_item(text_input)

    async def on_submit(self, interaction: discord.Interaction):
        #complete submit method
        print('Saving data...')