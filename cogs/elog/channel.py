import disnake
from disnake.ext import commands
from datetime import datetime
import pytz
import sqlite3


class Channel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    moscow_tz = pytz.timezone('Europe/Moscow')

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        guild = channel.guild
        async for entry in guild.audit_logs(limit=1, action=disnake.AuditLogAction.channel_create):
            creator = entry.user
            embed = disnake.Embed(color=disnake.Color.dark_gray(), title = "", description = "")
            embed.set_author(name=guild.name, icon_url=guild.icon.url)
            if isinstance(channel, disnake.TextChannel):
                embed.add_field(name = "", value = f':house: **Создан текстовый канал:** `{channel.name}`', inline=False)
            if isinstance(channel, disnake.VoiceChannel):
                embed.add_field(name = '', value = f':house: **Создан голосовой канал:** `{channel.name}`', inline = False)
            if isinstance(channel, disnake.CategoryChannel):
                embed.add_field(name = '', value = f':house: **Создана категория:** `{channel.name}`', inline = False)
            if isinstance(channel, disnake.ForumChannel):
                embed.add_field(name = '', value = f':house: **Создан форум:** `{channel.name}`', inline = False)
            if isinstance(channel, disnake.StageChannel):
                embed.add_field(name = '', value = f':house: **Создан проект:** `{channel.name}`', inline = False)
            embed.add_field(name="**Ответственный модератор:**", value = creator.mention)
            embed.set_footer(text=f"{guild.name} • Дата создания: {datetime.now(tz=self.moscow_tz).strftime('%B %d, %Y %H:%M')}")
            await disnake.utils.get(channel.guild.text_channels, id=1262100877066633267).send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        guild = channel.guild
        async for entry in guild.audit_logs(limit=1, action=disnake.AuditLogAction.channel_create):
            creator = entry.user
            embed = disnake.Embed(color=disnake.Color.dark_gray(), title = "", description = "")
            embed.set_author(name=guild.name, icon_url=guild.icon.url)
            if isinstance(channel, disnake.TextChannel):
                embed.add_field(name="", value=f':x: **Удален канал:** `{channel.name}`', inline=False)
            if isinstance(channel, disnake.VoiceChannel):
                embed.add_field(name = '', value = f':x: **Удалён голосовой канал:** `{channel.name}`', inline = False)
            if isinstance(channel, disnake.CategoryChannel):
                embed.add_field(name = '', value = f':x: **Удалена категория:** `{channel.name}`', inline = False)
            if isinstance(channel, disnake.ForumChannel):
                embed.add_field(name = '', value = f':x: **Удалён форум:** `{channel.name}`', inline = False)
            if isinstance(channel, disnake.StageChannel):
                embed.add_field(name = '', value = f':x: **Удалён проект:** `{channel.name}`', inline = False)
            embed.add_field(name="**Ответственный модератор:**", value = creator.mention)
            embed.set_footer(text=f"{guild.name} • Дата удаления: {datetime.now(tz=self.moscow_tz).strftime('%B %d, %Y %H:%M')}")
            await disnake.utils.get(channel.guild.text_channels, id=1262100877066633267).send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: disnake.abc.GuildChannel, after: disnake.abc.GuildChannel):
        log_channel = self.bot.get_channel(1262938908845408306)
        guild = after.guild
        async for entry in guild.audit_logs(limit = 1, action=disnake.AuditLogAction.channel_update):
            admin = entry.user
            embed = disnake.Embed(color = disnake.Color.dark_gray(), title = '', description = '')
            embed.set_author(name = guild.name, icon_url = guild.icon.url)
            if before.name != after.name:
                embed.add_field(name = '', value = f'**Измененно название канала с `{before.name}` на `{after.name}`**', inline = False)
            if before.topic != after.topic:
                embed.add_field(name = '', value = f'**Измененно описание канала с `{before.topic}` на `{after.topic}`**', inline = False)


# Доделать изменение настроек канала



            embed.add_field(name = '', value = f'**Ответственный модератор:** {admin.mention}', inline = False)
            embed.add_field(name = '', value = f'[Перейти к каналу]({before.jump_url})', inline = False)
            embed.set_footer(text=f"{guild.name} • Дата удаления: {datetime.now(tz=self.moscow_tz).strftime('%B %d, %Y %H:%M')}")
            await log_channel.send(embed=embed)




# голосовые каналы
        


def setup(bot):
    bot.add_cog(Channel(bot))