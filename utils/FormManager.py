import requests
import os
import json


class FormManager:
    def __init__(self, client):
        self.client = client
        self.userObject = None
        # "i" attribute is an iterable for the winner form, open to sugestions
        self.i = 0

    async def handleRequest(self, user):
        data = {
            "member": {
                "name": user.name,
                "lastname": user.lastName,
                "address_1": user.address1,
                "address_2": user.address2,
                "city": user.city,
                "state": user.state,
                "postal_code": user.postalCode,
                "country": user.country,
                "discord_id": user.discord_id,
                "discord_username": user.discordUsername,
                "avatar_url": user.avatar_url,
                "winner": user.isWinner
            },
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
        await self.userObject.send(
            f"```👤 Name: {user.name}\n👥 Lastname: {user.lastName}\n🏠 Address: {user.address1}\n🏠 Second Address(Optional): {user.address2}\n🏙️ City: {user.city}\n🗺️ State/Province: {user.state}\n📮 Postal: {user.postalCode}\n🌎 Country: {user.country}```"
        )

    async def formOver(self, user, view):
        """ this will call the printResult function and it will send a message to the user to confirm if everything is ok or not """
        await self.printResult(user)
        await self.userObject.send('Does this look correct?\nClick **\"Yes\"** to submit \nClick **\"No\"** for start over', view=view)
