import discord
import requests
from dotenv import load_dotenv
import json
import os
from discord.ext import commands
from discord import app_commands
from interactions.trivia import handle as handleTrivia


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