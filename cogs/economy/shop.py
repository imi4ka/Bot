import disnake
from disnake.ext import commands







class Shop(disnake.ui.StringSelect):
    def __init__(self):
        options = [
            disnake.SelectOption(label = '', description = '')
        ]
        super().__init__(placeholder = '', options = options)
    async def callback(self, interaction: disnake.MessageInteraction):
        if self.values[0] == '':
            await interaction.response.send_message(':', view = )
        
        elif self.values[0] == '':
            await interaction.response.send_message(':', view = )


class ShopB(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(ShopB(bot))