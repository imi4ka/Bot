import disnake
from disnake.ext import commands
import datetime 
from database.db import Db
import pytz

db = Db()
moscow_tz = pytz.timezone('Europe/Moscow')


class EternalRole(disnake.ui.StringSelect):
    def __init__(self):
        eternal_role_list = list(db.get_eternal_role())

        role = [role for role in guild.roles if role.name != '@everyone' if role.id != eternal_role_list]
        
        options = [
            disnake.SelectOption(label = f'{i.name} 🎭 ', value = f'{i.id}') for i in role
        ]
        super().__init__(placeholder = 'EternalRole', options = options)
    async def callback(self, interaction: disnake.MessageInteraction):
        db.insert_eternal_role(interaction.values[0])
        await interaction.response.edit_message(f'Роль с id`{interaction.values[0]}` добавлена как вечная роль.', view = None)

class TemporaryRole(disnake.ui.StringSelect):
    def __init__(self):
        options = [

        ]
        super().__init__(placeholder = '', options = options)
    async def callbakc(self, interaction: disnake.MessageInteraction):
        pass

class WorksRole(disnake.ui.StringSelect):
    def __init__(self):
        options = [

        ]
        super().__init__(placeholder = '', options = options)
    async def callbakc(self, interaction: disnake.MessageInteraction):
        pass

class ChangeCurrency(disnake.ui.StringSelect):
    def __init__(self):
        options = [

        ]
        super().__init__(placeholder = '', options = options)
    async def callbakc(self, interaction: disnake.MessageInteraction):
        pass

class EditBonuses(disnake.ui.StringSelect):
    def __init__(self):
        options = [

        ]
        super().__init__(placeholder = '', options = options)
    async def callbakc(self, interaction: disnake.MessageInteraction):
        pass

class EconomyDrop(disnake.ui.StringSelect):
    def __init__(self):
        options = [
            disnake.SelectOption(label = 'Изменить вечные роли', emoji = '🛎'),
            disnake.SelectOption(label = 'Изменить временные роли', emoji = '🛎'),
            disnake.SelectOption(label = 'Изменить рабочие роли', emoji = '🛎'),
            disnake.SelectOption(label = 'Изменить игровую валюту', emoji = '💵'),
            disnake.SelectOption(label = 'Настройка бонусов', emoji = '💰')
        ]
        super().__init__(placeholder = 'Economy', options = options)
    async def callback(self, interaction: disnake.MessageInteraction):
        if self.values[0] == 'Изменить вечные роли':
            await interaction.response.edit_message('', view = EternalRoleMenu())
        elif self.values[0] == 'Изменить временные роли':
            await interaction.response.edit_message('', view = TemporaryRoleMenu())
        elif self.values[0] == 'Изменить рабочие роли':
            await interaction.response.edit_message('', view = WorksRoleMenu())
        elif self.values[0] == 'Изменить игровую валюту':
            await interaction.response.edit_message('', view = ChangeCurrencyMenu())
        elif self.values[0] == 'Настройка бонусов':
            await interaction.response.edit_message('', view = EditBonusesMenu())

class Functionn(disnake.ui.StringSelect):
    def __init__(self):
        options = [
            disnake.SelectOption(label = '**Канал логов**', description = 'Выбрать канал для логов.', emoji = '🛡')
        ]
        super().__init__(placeholder = 'Settings function', options = options)

    async def callback(self, inter: disnake.MessageInteraction):
        await inter.response.edit_message('Выберите канал для отправки логов', view = ChannelsLogMenu())   

class ChannelsLog(disnake.ui.StringSelect):
    def __init__(self):
        channel = [channel for channel in guild.channels if channel.type == disnake.ChannelType.text]
        options = [
            disnake.SelectOption(label = f'{i.name}', description = f'{i.id}', emoji = '📃', value = f'{i.id}') for i in channel                                
        ]
        super().__init__(placeholder = 'Channel select', options = options)

    async def callback(self, inter: disnake.MessageInteraction):
        db.update_tabel_settings(inter.values[0])
        await inter.response.edit_message(f'Канал с ID {inter.values[0]} успешно выбран.', view = None)

class ChannelsLogMenu(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ChannelsLog())

class Automod(disnake.ui.StringSelect):
    def __init__(self):
        options = [
            disnake.SelectOption(label = '**Защита от спама**', description = 'Включить/выключить защиту от спама.', emoji = '🛡')
        ]
        super().__init__(placeholder = 'Settings automod', options = options)

    async def callback(self, inter: disnake.MessageInteraction):
        await inter.response.edit_message('1', view = None)

class AutomodSettingsMenu(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Automod())

class FunctionSettingsMenu(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Functionn())
    
class EconomySettingsMenu(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(EconomyDrop())

class EternalRoleMenu(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(EternalRole())

class TemporaryRoleMenu(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(TemporaryRole())

class WorksRoleMenu(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(WorksRole())

class ChangeCurrencyMenu(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ChangeCurrency())

class EditBonusesMenu(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(EditBonuses())

class Dropdown(disnake.ui.StringSelect):
    def __init__(self):
        options = [
            disnake.SelectOption(label = 'Логи', description = 'Настройка внутренних функций бота.', emoji = '⚙'),
            disnake.SelectOption(label = 'Модерация', description = 'Настройка функций автомода', emoji = '👑'),
            disnake.SelectOption(label = 'Экономика', description = 'Настройка экономики сервера', emoji = '🌌')
        ]
        super().__init__(placeholder = 'Settings', options = options) 

    async def callback(self, interaction: disnake.MessageInteraction):
        if self.values[0] == 'Логи':
            await interaction.response.edit_message('Настройки функций бота:', view = FunctionSettingsMenu())
        elif self.values[0] == 'Модерация':
            await interaction.response.edit_message('Настройка автомодерации ', view = AutomodSettingsMenu())
        elif self.values[0] == 'Экономика':
            await interaction.response.edit_message('1', view = EconomySettingsMenu())

class DropdownSettingsMenu(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Dropdown())

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name = 'settings', description = 'Команда для гибкой настройки бота.')
    async def settings(self, ctx: disnake.ApplicationCommandInteraction):
        global guild
        guild = ctx.guild
        await ctx.send('Настройка бота', view=DropdownSettingsMenu())



def setup(bot):
    bot.add_cog(Settings(bot))