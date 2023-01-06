import discord
from interactions.leaderboard import handle as handleLeaderboard

class SeasonButtons(discord.ui.View):
    def __init__(self, options = [], question = ''):
        super().__init__(timeout=180)
        self.options = options
        self.question = question
        self.build_buttons()
    
    def build_buttons(self):

        callbacks = {}
        for idx, option in enumerate(self.options):
            button = discord.ui.Button(label=option['name'], style=discord.ButtonStyle.blurple)

            button.callback = self.generate_callback(option = option)

            self.add_item(button)


    def generate_callback(self, option: str):
        
        async def validate_button(interaction: discord.Interaction):
                response = await handleLeaderboard(interaction, option['id'])
                embed = discord.Embed(title = option['name'], description = response['message'])
                embed.set_author(name = interaction.user, icon_url = interaction.user.avatar)
                await interaction.response.edit_message(embed = embed, content = None, view = None)
        
        return validate_button
