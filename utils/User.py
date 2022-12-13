import discord
from utils.FormManager import FormManager
from views.RegisterModal import RegisterModal

def getQuestionsList(fields):
    """ this function creates a list with only 'id' and 'questions' attributes """
    
    questions = []
    for x in fields:
        questions.append({"id": x['id'], "question": x['question']})
    return questions

class User(FormManager):

    def __init__(self, client):
        super().__init__(client)
        self.response = []
        self.isRegistered = False
        self.avatar_url = ''
        self.discord_id = ''
        self.username = ''

    async def setRemainingData(self, interaction: discord.Interaction, season: str=None, fields=None):
        """ this function sets the remaining data from discord and the CE Admin """

        # this will return only the questions inside the question object and store it in a list
        self.isRegistered = True
        self.questions=getQuestionsList(fields)

        self.nQuestions = len(self.questions)
        # this will return an array, that way is stored in an aux variable
        aux = interaction.user.name + '#' + interaction.user.discriminator,
        self.username = aux[0]
        self.avatar_url = str(interaction.user.avatar.url if interaction.user.avatar is not None else '')
        self.discord_id = str(interaction.user.id)
        self.user = await self.client.fetch_user(self.discord_id)
        self.season=season

    def clear(self):
        """ restart the iterator and the attributes of the participant """
        self.response.clear()
        self.nQuestions=len(self.questions)
        self.i = 0

    def saveResponse(self,res):
        """ save the user's response """
        self.response.append(res or '')