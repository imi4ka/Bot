import disnake
from disnake.ext import commands
from datetime import datetime
import pytz
from database.db import Db
db = Db()
def sinc_channel_id():
    channel_id = int(db.get_channel_id())
    return channel_id



class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    moscow_tz = pytz.timezone('Europe/Moscow')

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        guild = after.guild
        if before.author.bot:
            return
        if before.author.guild_permissions.administrator:
            embed = disnake.Embed(color=disnake.Color.dark_grey())
            embed.set_author(name=before.author.name, icon_url=before.author.display_avatar.url)
            embed.add_field(name="", value=f':pencil: **Сообщение от {before.author.mention} измененно в {before.channel.mention}.**', inline=False)
            embed.add_field(name="", value=f"[Перейти к сообщению]({before.jump_url})", inline=False)
            embed.add_field(name="Старое сообщение", value=f"```{before.content}```", inline=False)
            embed.add_field(name="Новое сообщение", value=f"```{after.content}```", inline=False)
            embed.set_footer(text=f"{guild.name} • Дата выхода: {datetime.now(tz=self.moscow_tz).strftime('%B %d, %Y %H:%M')}")
            channel = self.bot.get_channel(sinc_channel_id())
            await channel.send(embed=embed)



    @commands.Cog.listener()
    async def on_message_delete(self, message):
        guild = message.guild
        if message.author.bot:
            return
        if message.author.guild_permissions.administrator:
            embed = disnake.Embed(color=disnake.Color.dark_grey())
            embed.set_author(name=message.author.name, icon_url=message.author.display_avatar.url)
            embed.add_field(name="", value=f':pencil: **Сообщение от {message.author.mention} удалено в {message.channel.mention}.**', inline=False)
            embed.add_field(name="Удаленное сообщение", value=f"```{message.content}```", inline=False)
            embed.set_footer(text=f"{guild.name} • Дата выхода: {datetime.now(tz=self.moscow_tz).strftime('%B %d, %Y %H:%M')}")
            channel = self.bot.get_channel(sinc_channel_id())
            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Message(bot))