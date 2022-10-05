import discord
import requests
from dotenv import load_dotenv
import os
from discord.ext import commands
from discord import app_commands
from interactions.trivia import handle as handleTrivia


class RegisterModal(discord.ui.Modal):
    def __init__(self,title = 'Registration Proccess!', season = '',participant=object):
        super().__init__(title = title)
        self.season = season
        self.participant=participant
        self.start()
    
    def start (self):
        for question in self.participant.questions:
        
            answer =discord.ui.TextInput(label = question['question'], style = discord.TextStyle.short,required = True)
            
            
            self.add_item(answer)
            
            self.participant.saveResponse(answer)


        

    def cleanData(self):

        for index in range(len(self.participant.response)):
            self.participant.response[index]=self.participant.response[index].value

    async def on_submit(self, interaction: discord.Interaction):
        self.cleanData()
        try:
            response = await self.participant.handleRequest(self.participant)
            embed = discord.Embed(title = self.title, description = f"{self.participant.getOutputResult(self.participant)}**{response}**")
            embed.set_author(name = interaction.user, icon_url = interaction.user.avatar)
            await interaction.response.send_message(embed = embed, ephemeral = True)
            self.participant.clear()

        except Exception as err:
            print(err)
            await interaction.response.send_message(content=f"Something went wrong!!")
        

