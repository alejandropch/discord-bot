import discord
from utils.FormManager import FormManager
from views.YorNButtons import YorNButtons


class User(FormManager):

    def __init__(self, client):
        super().__init__(client)
        self.response = []
        self.isWinner = False
        self.avatar_url = ''
        self.discord_id = ''
        self.username = ''

    async def setRemanaingData(self, interaction: discord.Interaction, season: str, fields):
        """ this function sets the remaining data from discord and the CE Admin """

        # this will return only the questions inside the question object and store it in a list
        self.isWinner = True
        self.questions = list(map(lambda x: {"id": x['id'], "question": x['question']}, fields))
        self.nQuestions = len(self.questions)
        # this will return an array, that way is stored in an aux variable
        aux = interaction.user.name + '#' + interaction.user.discriminator,
        self.username = aux[0]
        self.avatar_url = str(interaction.user.avatar.url if interaction.user.avatar is not None else '')
        self.discord_id = str(interaction.user.id)
        self.user = await self.client.fetch_user(self.discord_id)
        self.season=season

    async def dmUser(self):

        # after the register command is sended....,
        # this should be a while loop

        while self.i < self.nQuestions:
            #def check(message):
                # if the bot respond a question for the user, it should be consider an error. Hence, if the one responding the message is not the winner user, it should be an error, open to suggestions
                # if message.author != self.discordUsername:
                #    return False

            await self.user.send(self.questions[self.i]['question'])
            res = (await self.client.wait_for("message")).content
            [isValid, errMessage] = self.errorHandler(res, True)
            if isValid == False:
                await self.user.send(f"Value provided is invalid. {errMessage}")
            else:
                self.nextQuestion()
                self.saveResponse(res)


        # end of while loop, if the iterator is equal or greater thant the value of total n° of questions
        view = YorNButtons(self)
        await self.formOver(self, view)
        return


    def clear(self):
        """ restart the iterator and the attributes of the winner user """
        self.response.clear()
        self.nQuestions=len(self.questions)
        self.i = 0
