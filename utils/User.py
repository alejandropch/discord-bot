import discord
from utils.FormManager import FormManager
from utils.YorNButtons import YorNButtons


class User(FormManager):

    def __init__(self, client):
        super().__init__(client)
        self.name = ''
        self.lastName = ''
        self.address1 = ''
        self.address2 = ''
        self.city = ''
        self.state = ''
        self.postalCode = ''
        self.discordUsername = ''
        self.country = ''
        self.discord_id = ''
        self.avatar_url = ''
        self.isWinner = False


        self.isWinner = True

        # this will return an array, thats way is stored in an aux variable
        aux = interaction.user.name + \
            '#' + interaction.user.discriminator,
        self.discordUsername = aux[0]

        self.avatar_url = str(
            interaction.user.avatar.url if interaction.user.avatar is not None else '')
        self.discord_id = str(interaction.user.id)
        # TODO: put this season id into the pivot table

    def clear(self):
        self.name = ''
        self.lastName = ''
        self.address1 = ''
        self.address2 = ''
        self.city = ''
        self.state = ''
        self.postalCode = ''
        self.country = ''
