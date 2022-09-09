import discord
from utils.FormManager import FormManager
from views.YorNButtons import YorNButtons


class User(FormManager):

    def __init__(self, client):
        super().__init__(client)
        self.response = []
        self.isWinner = False

    async def setRemanaingData(self, interaction: discord.Interaction, fields):
        """ this function sets the remaining data from discord and the CE Admin """

        self.questions = list(map(lambda x: x['question'], fields))
        self.nQuestions = len(self.questions)

        self.isWinner = True

        # this will return an array, that way is stored in an aux variable
        aux = interaction.user.name + \
            '#' + interaction.user.discriminator,
        self.discordUsername = aux[0]

        self.avatar_url = str(
            interaction.user.avatar.url if interaction.user.avatar is not None else '')
        self.discord_id = str(interaction.user.id)

        self.userObj = await self.client.fetch_user(self.discord_id)
        # TODO: put this season id into the pivot table

    async def dmUser(self):

        def check(message):
            # if the bot respond a question for the user, it should be consider an error. Hence, if the one responding the message is not the winner user, it should be an error, open to suggestions
            # if message.author != self.discordUsername:
            #    return False

            response = self.errorHandler(message.content)
            return False if response is False else True
        # if the iterator have the same value of the total n° of questions
        if self.i >= self.nQuestions:
            view = YorNButtons(self)
            await self.formOver(self, view)
            return

        await self.userObj.send(self.questions[self.i])
        res = (await self.client.wait_for("message", check=check)).content
        self.response.append(res or '')

    def clear(self):
        """ restart the iterator and the attributes of the winner user """
        self.response.clear()
        self.i = 0
