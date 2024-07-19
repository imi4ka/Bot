import disnake
from disnake.ext import commands
import pytz
import datetime
import sqlite3



class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    guild = None
    global conn
    conn = sqlite3.connect('tlogs.db')
    global c
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tlogs(channel_id TEXT)''')

    def dropdown(self):
        class Dropdown(disnake.ui.StringSelect):
            def __init__(self):
                options = [
                    disnake.SelectOption(label = 'Настройка функций', description = 'Настройка внутренних функций бота.', emoji = '⚙'),
                    disnake.SelectOption(label = 'Настройка автомодерации', description = 'Настройка функций автомода', emoji = '👑')
                ]
                super().__init__(placeholder = 'Settings', options = options)

            def functionn(self):
                class Functionn(disnake.ui.StringSelect):
                    def __init__(self):
                        options = [
                            disnake.SelectOption(label = '**Канал логов**', description = 'Выбрать канал для логов.', emoji = '🛡')
                        ]
                        super().__init__(placeholder = 'Settings function', options = options)

                    def channelsl(self):
                        class Channelsl(disnake.ui.StringSelect):
                            def __init__(self):
                                channel = [channel for channel in guild.channels if channel.type == disnake.ChannelType.text]
                                options = [
                                    disnake.SelectOption(label = f'{i.name}', description = f'{i.id}', emoji = '📃', value = f'{i.id}') for i in channel                                
                                ]
                                super().__init__(placeholder = 'Channel select', options = options)

                            async def callback(self, inter: disnake.MessageInteraction):
                                c.execute("UPDATE tlogs SET channel_id = ?", (inter.values[0],))
                                conn.commit()
                                await inter.response.send_message(f'Канал с ID {inter.values[0]} успешно выбран.')
                        return Channelsl
                    
                    class ChannelslMenu(disnake.ui.View):
                        def __init__(self, channelsl):
                            super().__init__()
                            self.add_item(channelsl())

                    async def callback(self, inter: disnake.MessageInteraction):
                        channelsl = self.channelsl()
                        await inter.message.edit('Выберите канал для отправки логов', view = self.ChannelslMenu(channelsl))                 
                return Functionn
            
            def automod(self):
                class Automod(disnake.ui.StringSelect):
                    def __init__(self):
                        options = [
                            disnake.SelectOption(label = '**Защита от спама**', description = 'Включить/выключить защиту от спама.', emoji = '🛡')
                        ]
                        super().__init__(placeholder = 'Settings automod', options = options)

                    async def callback(self, inter: disnake.MessageInteraction):
                        await inter.response.send_message('1')
                return Automod
            
            class FunctionSettingsMenu(disnake.ui.View):
                def __init__(self, Functionn):
                    super().__init__()
                    self.add_item(Functionn())

            class AutomodSettingsMenu(disnake.ui.View):
                def __init__(self, Automod):
                    super().__init__()
                    self.add_item(Automod())

            async def callback(self, inter: disnake.MessageInteraction):
                functionn = self.functionn()
                automod = self.automod()
                if self.values[0] == 'Настройка функций':
                    await inter.message.edit('Настройки функций бота:', view = self.FunctionSettingsMenu(functionn))
                elif self.values[0] == 'Настройка автомодерации':
                    await inter.message.edit('Настройка автомодерации ', view = self.AutomodSettingsMenu(automod))
        return Dropdown
    
    class DropdownMenu(disnake.ui.View):
        def __init__(self, Dropdown):
            super().__init__()
            self.add_item(Dropdown())

    @commands.slash_command(name = 'settings', description = 'Команда для гибкой настройки бота.')
    async def settings(self, ctx: disnake.ApplicationCommandInteraction):
        global guild
        guild = ctx.guild
        dropdown = self.dropdown()
        await ctx.send('Настройка бота', view=self.DropdownMenu(dropdown))

def setup(bot):
    bot.add_cog(Settings(bot))