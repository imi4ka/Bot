import disnake
from disnake.ext import commands
from datetime import datetime
from database.db import Db
import pytz

moscow_tz = pytz.timezone('Europe/Moscow')
db = Db()

class Embeds_message():
    def main(self, ctx: disnake.ApplicationCommandInteraction, member: disnake.Member):
        embed = disnake.Embed( 
            color = disnake.Color.dark_gray(), 
            description = 'Взаимодействуйте с выпадающим меню выбора, чтобы настроить сервер.', 
            title = '**Настройка модулей бота.**'
            )
        embed.set_footer(text=f"Запрос выполнил {ctx.author} • Сегодня, в {datetime.now(tz = moscow_tz).strftime('%H:%M')}", icon_url = member.display_avatar.url)
        return embed
    
    def audit_logs_channel(self, member: disnake.Member):
        embed = disnake.Embed( 
            color = disnake.Color.dark_gray(), 
            description = 'Это различные типы событий, которые срабатывают при удалении сообщений, использовании команд и действиях по модерации.', 
            title = '**Журнал действий.**'
            )
        embed.add_field(name = '*Используйте кнопки для управления настройками.*', value = '', inline = False)
        embed.set_footer(text=f"Запрос выполнил {member.name} • Сегодня, в {datetime.now(tz = moscow_tz).strftime('%H:%M')}", icon_url = member.display_avatar.url)
        return embed

    def shop_settings(self, member: disnake.Member):
        embed = disnake.Embed( 
            color = disnake.Color.dark_gray(), 
            description = '', 
            title = '**Экономика.**'
            )
        embed.add_field(name = '', value = '', inline = False)
        embed.set_footer(text=f"Запрос выполнил {member.name} • Сегодня, в {datetime.now(tz = moscow_tz).strftime('%H:%M')}", icon_url = member.display_avatar.url)
        return embed

emb = Embeds_message()

class EternalRole(disnake.ui.StringSelect):
    def __init__(self):
        list = db.get_economy_all_role_id()
        for list in list:
            list = [list[0], list[1], list[2]]

        if list != None:
            self.eternal_role_list = list
        else:
            self.eternal_role_list = []
        role = [role for role in guild.roles if role.name != '@everyone']
        options = [
            disnake.SelectOption(label = f'{i.name} 🎭 ', value = f'{i.id}') for i in role if str(i.id) not in self.eternal_role_list
        ]
        super().__init__(placeholder = 'EternalRole', options = options)
    async def callback(self, interaction: disnake.MessageInteraction):
        db.insert_economy_eternal_role(interaction.values[0])
        await interaction.response.edit_message(f'Роль с id`{interaction.values[0]}` добавлена как вечная роль.', view = EternalRoleMenu())

class TemporaryRole(disnake.ui.StringSelect):
    def __init__(self):
        list = db.get_economy_all_role_id()
        for list in list:
            list = [list[0], list[1], list[2]]

        if list != None:
            self.eternal_role_list = list
        else:
            self.eternal_role_list = []
        role = [role for role in guild.roles if role.name != '@everyone']
        options = [
            disnake.SelectOption(label = f'{i.name} 🎭 ', value = f'{i.id}') for i in role if str(i.id) not in self.eternal_role_list
        ]
        super().__init__(placeholder = 'EternalRole', options = options)
    async def callback(self, interaction: disnake.MessageInteraction):
        db.insert_economy_temporary_role(interaction.values[0])
        await interaction.response.edit_message(f'Роль с id`{interaction.values[0]}` добавлена как временная роль.', view = TemporaryRoleMenu)  

class WorksRole(disnake.ui.StringSelect):
    def __init__(self):
        list = db.get_economy_all_role_id()
        for list in list:
            list = [list[0], list[1], list[2]]

        if list != None:
            self.eternal_role_list = list
        else:
            self.eternal_role_list = []
        role = [role for role in guild.roles if role.name != '@everyone']
        options = [
            disnake.SelectOption(label = f'{i.name} 🎭 ', value = f'{i.id}') for i in role if str(i.id) not in self.eternal_role_list
        ]
        super().__init__(placeholder = 'EternalRole', options = options)
    async def callback(self, interaction: disnake.MessageInteraction):
        db.insert_economy_worker_role(interaction.values[0])
        await interaction.response.edit_message(f'Роль с id`{interaction.values[0]}` добавлена как вечная роль.', view = WorksRoleMenu())

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
 
class ChannelsLog(disnake.ui.StringSelect):
    def __init__(self):
        channel = [channel for channel in guild.channels if channel.type == disnake.ChannelType.text]
        options = [
            disnake.SelectOption(label = f'{i.name}', description = f'{i.id}', emoji = '📃', value = f'{i.id}') for i in channel                                
        ]
        super().__init__(placeholder = 'Выбрать канал', options = options)

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
            disnake.SelectOption(label = 'Журнал действий', description = 'Настройка внутренних функций бота.', emoji = '⚙'),
            disnake.SelectOption(label = 'Модерация', description = 'Настройка функций автомода', emoji = '👑'),
            disnake.SelectOption(label = 'Экономика', description = 'Настройка экономики сервера', emoji = '🌌')
        ]
        super().__init__(placeholder = 'Настройки сервера', options = options) 

    async def callback(self, interaction: disnake.MessageCommandInteraction):
        if self.values[0] == 'Журнал действий':
            await interaction.response.edit_message(embed = emb.audit_logs_channel(interaction.user) , view = ChannelsLogMenu())
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
        await ctx.send(embed = emb.main(ctx, ctx.author) , view=DropdownSettingsMenu())



def setup(bot):
    bot.add_cog(Settings(bot))