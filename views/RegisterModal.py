import discord
from discord.ext import commands
from discord import app_commands

class RegisterModal(discord.ui.Modal):
    def __init__(self,title = 'Registration Proccess!', participant=object, one_season=bool):
        super().__init__(title = title)
        self.participant=participant
        self.one_season=one_season
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
            if self.one_season == True:
                await interaction.response.send_message(embed = embed, ephemeral = True)
            else:
                await interaction.response.edit_message(embed = embed, content = None, view = None)

            self.participant.clear()

        except Exception as err:
            print(err)
            await interaction.response.send_message(content="Something went wrong!!",ephemeral = True)
        

