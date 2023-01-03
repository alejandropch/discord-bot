import requests
import os
import json
from utils.joinAnswers import joinAnswers
from utils.getQuestionsList import getQuestionsList
from utils.seasons import getFields


class FormManager:
    def __init__(self):
        self.user = None
        # "i" attribute is an iterable for the participant form, open to sugestions
        self.i = 0
        self.nQuestions = 0
        self.questions = []
        self.season_id = ''

    async def handleRequest(self):

        answers = joinAnswers(self) if len(self.questions) != 0 else [{'id': '', "answer": []}]
        data = ''
        if self.avatar_url == '':
            data = {
                "season_id": self.season_id,
                "member": {
                    "id": self.discord_id,
                    "username": self.username,
                },
                "answers": answers
            }
        else:
            data = {
                "season_id": self.season_id,
                "member": {
                    "id": self.discord_id,
                    "username": self.username,
                    "avatar_url": self.avatar_url,
                },
                "answers": answers
            }

        value = requests.post(os.environ["API_URL"] + '/seasons/register', data=json.dumps(data), headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.environ["API_KEY"]
        })

        try:
            value = value.json()

            try:
                if value['status'] == 'error':
                    raise Exception
            except Exception:
                print(value)
                return "Something went wrong!"

            if len(self.questions) > 0:
                return "Form sent successfully!"
            else:
                return "You have successfully registered!"

        except json.decoder.JSONDecodeError:
            print("json empty")
            return "Something went wrong!"

    def getOutputResult(self, participant):
        """ print all the information the user has given"""
        output = ''
        for i in range(self.nQuestions):
            output = output + \
                f"**🔻 {participant.questions[i]['question']}** \n 🔸\t{participant.response[i]}\n"

        return output

    async def setListOfQuestions(self, season_id):
        response = await getFields(season_id)
        self.questions = getQuestionsList(fields = response['data'])
        self.setNumberOfQuestions()

    def setNumberOfQuestions(self):
        self.nQuestions = len(self.questions)

    def setSeasonID(self, season_id: str):
            self.season_id = season_id