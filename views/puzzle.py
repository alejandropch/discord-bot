import discord
import requests
from dotenv import load_dotenv
import json
import os
from discord.ext import commands
from discord import app_commands
from utils.seasons import getRandomQuestion
from interactions.trivia import handle as handleTrivia


puzzle_image= "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRMEH6Ej19TTqtfVxSOyxywMrSLvylrk0Vieg&usqp=CAU"

class Puzzle(discord.ui.View):
    def __init__(self, options = []):
        super().__init__(timeout=180)
        self.options = options
        self.build_buttons()
    
    def build_buttons(self):
        for idx, option in enumerate(self.options):
            button = discord.ui.Button(label=option['name'], style=discord.ButtonStyle.blurple)
            button.callback = self.generate_callback(option = option)
            self.add_item(button)


    def generate_callback(self, option: str): # when an option (season) is clicked
        
        async def validate_button(interaction: discord.Interaction):
            question = await getRandomQuestion(season_id=option['id'], user=interaction.user, puzzle=True)
            if question['status'] == 'success':
                await showPuzzle(interaction, question)
            else:
                await interaction.response.send_message(question['message'], ephemeral=True)
        
        return validate_button

async def showPuzzle(interaction, question):
    button = Button(title= question['data']['question'], event=question['data']['event'])
    dict_content = json.loads(question['data']['question'])
    embed = discord.Embed.from_dict(dict_content)
    await interaction.response.send_message(view=button, embed=embed, ephemeral=True)

class Button(discord.ui.View):
    def __init__(self, title='', event = ''):
        super().__init__(timeout=180)
        self.event = event
        self.build_buttons()
    
    def build_buttons(self):
        button = discord.ui.Button(label="Answer it!", style=discord.ButtonStyle.blurple)
        button.callback = self.generate_callback()
        self.add_item(button)


    def generate_callback(self):

        async def validate_button(interaction: discord.Interaction):
            await interaction.response.send_modal(PuzzleModal(title= self.event['name'], event=self.event))

        return validate_button

class PuzzleModal(discord.ui.Modal):
    def __init__(self, title = 'Puzzle!',  event = ''):
        super().__init__(title = title)
        self.event = event

    answer = discord.ui.TextInput(label = 'Answer', style = discord.TextStyle.short, required = True)

    async def on_submit(self, interaction: discord.Interaction):
        
        response = await handleTrivia(interaction, self.event, self.answer.value)
        embed = discord.Embed(title = self.event['name'], description = f"**{self.answer.label}**\n{self.answer}\n\n**{response}**")
        embed.set_author(name = interaction.user, icon_url = interaction.user.avatar)
        await interaction.response.send_message(embed = embed, ephemeral = True)


