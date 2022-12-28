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


class RegisterModal(discord.ui.Modal):
    def __init__(self, title='Registration Proccess!', participant: User = object, season_id: int = int):
        super().__init__(title=title)
        self.participant = participant
        self.season_id = season_id
        print(self.season_id)
        self.start()

    def start(self):
        for question in self.participant.questions:
            answer = discord.ui.TextInput(
                label=question['question'], style=discord.TextStyle.short, required=True)
            self.add_item(answer)
            self.participant.saveResponse(answer)

    async def orginizeDataPrevSubmit(self):
        # exists = await userExists(interaction=discord.Interaction,season_id=self.season_id)
        # if exists["status"]=="error":
        #    raise NameError(exists["message"])

        for index in range(len(self.participant.response)):
            self.participant.response[index] = self.participant.response[index].value

    async def on_submit(self, interaction: discord.Interaction):
        try:
            await self.orginizeDataPrevSubmit()
            fields = await getFields(self.season_id)

            await self.participant.setRemainingData(interaction, self.season_id, fields['data'])

            response = await self.participant.handleRequest(self.participant)
            embed = discord.Embed(
                title=self.title, description=f"{self.participant.getOutputResult(self.participant)}**{response}**")
            embed.set_author(name=interaction.user,
                             icon_url=interaction.user.avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

            # clear participant's data since the register is already made
            self.participant.clear()

        except Exception as err:
            print(err)
            await interaction.response.send_message(content="Something went wrong!!", ephemeral=True)
