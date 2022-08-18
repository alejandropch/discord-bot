import discord
import requests
from dotenv import load_dotenv
import json
import os
from discord.ext import commands
from discord import app_commands

class Buttons(discord.ui.View):
    def __init__(self, options = []):
        super().__init__(timeout=180)
        self.options = options
        self.build_buttons()
    
    def build_buttons(self):

        callbacks = {}
        for idx, option in enumerate(self.options):
            button = discord.ui.Button(label=option, style=discord.ButtonStyle.blurple)

            button.callback = self.generate_callback(option = option)

            self.add_item(button)


    def generate_callback(self, option: str):
        
        async def validate_button(interaction: discord.Interaction):
                await interaction.response.edit_message(content=f"You chose: " + option, view = None)
        
        return validate_button


