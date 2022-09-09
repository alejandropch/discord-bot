import discord
from discord.ext import commands
from discord import app_commands
from pickle import FALSE
from tabnanny import check
from urllib import response
import discord
import os
from discord.ext import commands
from discord import app_commands


class YorNButtons(discord.ui.View):
    def __init__(self, winner, timeout=None):
        """
        Parameters
        ----------
        winner : object
            the User object
        timeout : int, optional
            set the timeout for these buttons
        """
        super().__init__(timeout=timeout)
        self.value = None
        self.winner = winner

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green, custom_id="yes")
    async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        if self.value == None:
            try:
                await self.winner.handleRequest(self.winner)

                await interaction.response.send_message(content="Form sent successfully!")
                self.winner.clear()
                self.value = True
            except:
                await interaction.response.send_message(content='Something has broken, we are fixing it!')
            return

        else:
            await interaction.response.edit_message(content=f"You already clicked this button!!")
        return

    @discord.ui.button(label="No", style=discord.ButtonStyle.red, custom_id="no")
    async def no_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        if self.value == None:
            await interaction.response.send_message(content=f"let's start again")
            self.winner.clear()
            self.value = False
            return await self.winner.dmUser()
        else:
            await interaction.response.edit_message(content=f"You already clicked this button!!")
        return
