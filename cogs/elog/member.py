import disnake
from disnake.ext import commands
from datetime import datetime
import pytz
from database.db import Db
db = Db()
global channel_id
channel_id = int(db.get_channel_id())

class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    moscow_tz = pytz.timezone('Europe/Moscow')



    @commands.Cog.listener()
    async def on_member_update(self, before, after):
            guild = after.guild
            embed = disnake.Embed(color=disnake.Color.dark_gray(), title = "", description = f'**{after.mention} Был обновлен.**')
            embed.set_author(name=guild.name, icon_url=guild.icon.url)
            embed.set_thumbnail(url=after.display_avatar.url)
            if before.roles != after.roles:

                added_roles = [role for role in after.roles if role not in before.roles]
                if added_roles:
                    added_roles_text = "\n".join([role.mention for role in added_roles])
                    embed.add_field(name="**:white_check_mark: Роли добавлены:**", value=added_roles_text, inline=False)

                removed_roles = [role for role in before.roles if role not in after.roles]
                if removed_roles:
                    removed_roles_text = "\n".join([role.mention for role in removed_roles])
                    embed.add_field(name="**:no_entry: Роли удалены:**", value=removed_roles_text, inline=False)

            if before.nick != after.nick:
                embed.add_field(name = '', value = f'**Изменённ никнейм участника с** `{before.nick}` **на** `{after.nick}`')

            embed.set_footer(text=f"{guild.name} • Дата изменения: {datetime.now(tz=self.moscow_tz).strftime('%B %d, %Y %H:%M')}")
            channel = self.bot.get_channel(channel_id)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        async for entry in guild.audit_logs(limit=1, action=disnake.AuditLogAction.ban):
            admin = entry.user
            reason = entry.reason if entry.reason else "Не указана"

            embed = disnake.Embed(color=disnake.Color.dark_gray(), title = "", description = "")
            embed.set_author(name=guild.name, icon_url=guild.icon.url)
            embed.set_thumbnail(url=user.avatar.url)
            embed.add_field(name="", value=f'{user.mention} **Был забанен на сервере по причине:** `{reason}`.', inline=False)
            embed.add_field(name="**Ответственный модератор:**", value = admin.mention)
            embed.set_footer(text=f"{guild.name} • Дата бана: {datetime.now(tz=self.moscow_tz).strftime('%B %d, %Y %H:%M')}")
        channel = self.bot.get_channel(channel_id)  # Замените на ID нужного канала
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        async for entry in guild.audit_logs(limit=1, action=disnake.AuditLogAction.unban):
            admin = entry.user
            
        embed = disnake.Embed(color=disnake.Color.dark_gray(), title = "", description = "")
        embed.set_author(name=guild.name, icon_url=guild.icon.url)
        embed.set_thumbnail(url=user.avatar.url)
        embed.add_field(name="", value=f'{user.mention} **Был разбанен.**', inline=False)
        embed.add_field(name="**Ответственный модератор:**", value = admin.mention)
        embed.set_footer(text=f"{guild.name} • Дата разбана: {datetime.now(tz=self.moscow_tz).strftime('%B %d, %Y %H:%M')}")
        channel = self.bot.get_channel(channel_id)  # Замените на ID нужного канала
        await channel.send(embed=embed)
    
def setup(bot):
    bot.add_cog(Member(bot))