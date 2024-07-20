import disnake
from disnake.ext import commands
from datetime import datetime
import pytz
from database.db import Db

class Thread(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    moscow_tz = pytz.timezone('Europe/Moscow')


    db = Db()
    global channel_id
    channel_id = int(db.get_channel_id())

    @commands.Cog.listener()
    async def on_thread_create(self, thread: disnake.Thread):
        guild = thread.guild
        embed = disnake.Embed(color = disnake.Color.dark_gray(), title = '', description = '')
        embed.set_author(name = guild.name, icon_url = guild.icon.url)
        embed.add_field(name = '', value = f'**Создана ветка** `{thread.name}` **в канале** `{thread.parent.name}`', inline = False)
        embed.add_field(name = '', value = f'**Создатель ветки:** {thread.owner.mention}', inline = False)
        embed.add_field(name = '', value = f'[Перейти к ветке]({thread.jump_url})', inline = False)
        embed.set_footer(text=f"{guild.name} • Дата создания: {datetime.now(tz=self.moscow_tz).strftime('%B %d, %Y %H:%M')}")
        log_channel = self.bot.get_channel(channel_id)
        if log_channel is not None:
            await log_channel.send(embed=embed)
        else:
            print(f"Не удалось найти канал с ID {channel_id}")

    @commands.Cog.listener()
    async def on_thread_delete(self, thread):
        guild = thread.guild
        embed = disnake.Embed(color = disnake.Color.dark_gray(), title = '', description = '')
        embed.set_author(name = guild.name, icon_url = guild.icon.url)
        embed.add_field(name = '', value = f'**Удаленна ветка** `{thread.name}` **из канала** `{thread.parent.name}`', inline = False)
        embed.add_field(name = '', value = f'**Создатель ветки:** {thread.owner.mention}', inline = False)
        embed.add_field(name = '', value = f'**Общее кол-во сообщений в ветке:** {thread.message_count}')
        embed.set_footer(text=f"{guild.name} • Дата удаления: {datetime.now(tz=self.moscow_tz).strftime('%B %d, %Y %H:%M')}")
        log_channel = self.bot.get_channel(channel_id)
        await log_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Thread(bot))
