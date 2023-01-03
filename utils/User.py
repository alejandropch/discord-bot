import discord
from utils.FormManager import FormManager
from utils.getQuestionsList import getQuestionsList


class User(FormManager):

    def __init__(self, interaction: discord.Interaction):
        super().__init__(interaction)
        self.response = []
        self.avatar_url = ''
        self.discord_id = ''
        self.username = ''
        self.setUserData(interaction)

    def setUserData(self, interaction: discord.Interaction):
        self.deleteResponse()

        # this will return an array, that way is stored in an aux variable
        aux = interaction.user.name + '#' + interaction.user.discriminator,

        self.username = aux[0]
        self.avatar_url = str(interaction.user.avatar.url if interaction.user.avatar is not None else '')
        self.discord_id = str(interaction.user.id)

    def deleteResponse(self):
        """ Clear the response list """
        self.response.clear()
        self.i = 0

    def saveResponse(self, res):
        """ save the user's response """
        self.response.append(res or '')
