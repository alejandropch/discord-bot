import requests
import os
import json
import re
from utils.joinAnswers import joinAnswers

class FormManager:
    def __init__(self, client):
        self.client = client
        self.userObj = None
        # "i" attribute is an iterable for the winner form, open to sugestions
        self.i = 0
        self.nQuestions = 0
        self.questions = []
        self.season = ''

    async def handleRequest(self, user):
        
        answers =joinAnswers(self)

        data = {
            "season": user.season,
            "member": {
                "id": user.discord_id,
                "username": user.username,
                "avatar_url": user.avatar_url,
            },
            "answers": answers
        }

        value = requests.post(os.environ["API_URL"] + '/participants/', data=json.dumps(data), headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + os.environ["API_KEY"]
        })

        try:
            value = value.json()
            print(value)
        except json.decoder.JSONDecodeError:
            print("json empty")

        return

    def nextQuestion(self):
        """ this function will sum the i atribute plus one (like i++) """
        self.i += 1

    async def printResult(self, user):
        """ print all the information the user has given"""
        output = '```'
        for i in range(self.nQuestions):
            output = output + \
                f"🔻 {user.questions[i]} \n🔸\t{user.response[i]}\n"

        output = output+"```"
        await self.userObj.send(output)

    async def formOver(self, user, view):
        """ this will call the printResult function and it will send a message to the user to confirm if everything is ok or not """
        await self.printResult(user)
        await self.userObj.send('Does this look correct?\nClick **\"Yes\"** to submit \nClick **\"No\"** for start over', view=view)

    def errorHandler(self, message, getMsg=False):
        err = None
        if len(message) > 255:
            err = "Please do not use more than 255 characters"
        if re.match("^[-\w\s.,']*$", message) is None:
            err = "Please do not use special characters"
        if err is None:
            if getMsg is True:
                return [True, '']
            else:
                return True
        else:
            if getMsg is True:
                return [False, err]
            else:
                return False
