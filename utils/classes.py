import discord

import requests
import os
import json
from utils.seasons import getFields
from utils.seasons import assignRole
from utils.seasons import handleSuccessfulResponse


class FormManager:
    def __init__(self):
        self.user = None
        self.nQuestions = 0
        self.questions = []
        self.season_id = ''
        self.role_id = ''

    async def handleRequest(self,season_id):

        self.setSeasonID(season_id)
        answers = self.joinAnswers()
        
        data = {
            "season_id": self.season_id,
            "member": {
                "id": self.discord_id,
                "username": self.username,
                **({"avatar_url":self.avatar_url } if self.avatar_url else {}),
            },
            "answers": answers
        }

        value = requests.post(os.environ["API_URL"] + '/seasons/register', data=json.dumps(data), headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.environ["API_KEY"]
        })

        try:
            value = value.json()
            if value['status'] == 'error':
                return "Something went wrong!"
            
            # after successfully register a participant, it should assign it a role 
            await assignRole(discord_id=self.discord_id, role_id=self.role_id)

            return handleSuccessfulResponse(self.questions)

        except json.decoder.JSONDecodeError:
            print("json empty")
            return "Something went wrong!"
        except Exception as err:
            print(err)
            return "Oops! Seems the role of the season was not assigned to you."

    def getOutputResult(self, participant):
        """ print all the information the user has given"""
        output = ''
        for i in range(self.nQuestions):
            output = output + \
                f"**🔻 {participant.questions[i]['question']}** \n 🔸\t{participant.response[i]}\n"

        return output

    async def setListOfQuestions(self, season_id):
        
        response = await getFields(season_id)
        if response['status'] != 'success':
            raise Exception(response['message'])
        
        fields = response['data']

        for x in fields:
            self.questions.append({"id": x['id'], "question": x['question']})

        self.setNumberOfQuestions()

    def setNumberOfQuestions(self):
        self.nQuestions = len(self.questions)

    def setSeasonID(self, season_id: str):
            self.season_id = season_id

    def setRoleID(self, role_id: str):
            self.role_id = int(role_id)

    def joinAnswers(self):
        """ collects all questions' id with its answer if the form have questions, if not, it will return an array with empty attributes """

        if len(self.questions) == 0 :
            return [{'id': '', "answer": []}]

        answers=[]
        for i in range(self.nQuestions):
            answers.append({
                "id": str(self.questions[i]["id"]),
                "answer": self.response[i]
        })
        return answers


class User(FormManager):

    def __init__(self, interaction: discord.Interaction):
        super().__init__()
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

    def saveResponse(self, res):
        """ save the user's response """
        self.response.append(res or '')