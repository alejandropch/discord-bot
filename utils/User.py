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

    async def setRemanaingData(self, interaction: discord.Interaction, season: str):
        """ this function does fill the remaining data from discord that must be sent to the CE admin"""

        self.isWinner = True

        # this will return an array, thats way is stored in an aux variable
        aux = interaction.user.name + \
            '#' + interaction.user.discriminator,
        self.discordUsername = aux[0]

        self.avatar_url = str(
            interaction.user.avatar.url if interaction.user.avatar is not None else '')
        self.discord_id = str(interaction.user.id)

        self.userObject = await self.client.fetch_user(self.discord_id)
        # TODO: put this season id into the pivot table

    async def dmUser(self):

        def check(message):
            # if the bot respond a question for the user, it should be consider an error. Hence, if the one responding the message is not the winner user, it should be an error
            if message.author != self.discordUsername:
                False

            response = self.errorHandler(message.content)
            return False if response is False else True

        if self.i == 0:
            await self.userObject.send("What is your first name?")

            name = (await self.client.wait_for("message", check=check)).content
            if name == "":
                return

            self.name = name or ''

        if self.i == 1:
            await self.userObject.send("What is your last name?")
            lastName = (await self.client.wait_for("message", check=check)).content
            if lastName == "":
                return
            self.lastName = lastName or ''

        if self.i == 2:
            await self.userObject.send("Please provide your Address (first line)")
            address1 = (await self.client.wait_for("message", check=check)).content
            if address1 == "":
                return
            self.address1 = address1 or ''

        if self.i == 3:
            await self.userObject.send("Please provide your Address 2 (if none, please type '-')")
            address2 = (await self.client.wait_for("message", check=check)).content

            if address2 == "" or address2.strip() == "-":
                return
            self.address2 = address2 or ''

        if self.i == 4:
            await self.userObject.send("Please provide your City")
            city = (await self.client.wait_for("message", check=check)).content
            if city == "":
                return
            self.city = city or ''

        if self.i == 5:
            await self.userObject.send("Please provide your State/Province")
            state = (await self.client.wait_for("message", check=check)).content
            if state == "":
                return
            self.state = state or ''

        if self.i == 6:
            await self.userObject.send("Please provide your Postal Code")
            postalCode = (await self.client.wait_for("message", check=check)).content
            if postalCode == "":
                return
            self.postalCode = postalCode or ''

        if self.i == 7:
            await self.userObject.send("Please provide your Country")
            country = (await self.client.wait_for("message", check=check)).content
            if country == "":
                return
            self.country = country or ''

        if self.i == 8:
            view = YorNButtons(self)
            await self.formOver(self, view)

    def clear(self):
        """ restart the iterator and the attributes of the winner user """
        self.name = ''
        self.lastName = ''
        self.address1 = ''
        self.address2 = ''
        self.city = ''
        self.state = ''
        self.postalCode = ''
        self.country = ''
        self.i = 0
