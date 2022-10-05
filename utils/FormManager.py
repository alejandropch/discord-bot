import requests
import os
import json
from utils.joinAnswers import joinAnswers

class FormManager:
    def __init__(self, client):
        self.client = client
        self.user = None
        # "i" attribute is an iterable for the participant form, open to sugestions
        self.i = 0
        self.nQuestions = 0
        self.questions = []
        self.season = ''

    async def handleRequest(self, user):
        
        answers =joinAnswers(self) if user.nQuestions !=0 else [{'id':'',"answer":[]}]

        data = {
            "season": user.season,
            "member": {
                "id": user.discord_id,
                "username": user.username,
                "avatar_url": user.avatar_url,
            },
            "answers": answers
        }
        
        value = requests.post(os.environ["API_URL"] + '/season/register', data=json.dumps(data), headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.environ["API_KEY"]
        })

        try:
            value = value.json()
            print(value)
            return "Form sent successfully!"
        except json.decoder.JSONDecodeError:
            print("json empty")

        return "Something went wrong!"

    def getOutputResult(self,participant):
        """ print all the information the user has given"""
        output = ''
        for i in range(self.nQuestions):
            output = output + \
                f"**🔻 {participant.questions[i]['question']}** \n 🔸\t{participant.response[i]}\n"

        return output

