import discord
from discord.ext import commands
from discord import app_commands
from utils.classes import Participant
import markdownify


class RulesButtons(discord.ui.View):
    def __init__(self, options=[]):
        super().__init__(timeout=180)
        self.options = options
        self.build_buttons()

    def build_buttons(self):
        for idx, option in enumerate(self.options):
            button = discord.ui.Button(
                label=option['name'], style=discord.ButtonStyle.blurple)

            button.callback = self.generate_callback(option=option)

            self.add_item(button)

    def generate_callback(self, option: str):

        async def validate_button(interaction: discord.Interaction):
          await showTC(interaction,option)

        return validate_button


async def showTC(interaction, option):
    html = str(option['terms'])
    text = markdownify.markdownify(html, heading_style="ATX")
    embed = discord.Embed(title="Terms & Conditions", description=f"{text}")
    embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
    await interaction.response.send_message(embed=embed, ephemeral=True)

