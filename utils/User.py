import discord
import os


class User:

    def __init__(self):
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

    async def printResult(self, user):
        await user.send(
            f"```👤 Name: {self.name}\n👥 Lastname: {self.lastName}\n🏠 Address: {self.address1}\n🏠 Second Address(Optional): {self.address2}\n🏙️ City: {self.city}\n🗺️ State/Province: {self.state}\n📮 Postal: {self.postalCode}\n🌎 Country: {self.country}```"
        )

    def setRemanaingData(self, user):
        """ print(user) """
        self.isWinner = True
        self.discordUsername = user.name

    def clear(self):
        self.name = ''
        self.lastName = ''
        self.address1 = ''
        self.address2 = ''
        self.city = ''
        self.state = ''
        self.postalCode = ''
        self.country = ''


"""     def isFufilled(self):
        for attr in self.__dict__.keys():
            if attr == '':
                print(attr)
                return False
        return True """
