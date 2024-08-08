import disnake
from disnake.ext import commands
from datetime import datetime
import pytz
from database.db import Db
db = Db()
def sinc_channel_id():
    channel_id = int(db.get_channel_id())
    return channel_id


class RoleLog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    moscow_tz = pytz.timezone('Europe/Moscow')



    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        guild = role.guild
        async for entry in guild.audit_logs(limit=1, action=disnake.AuditLogAction.role_create):
            admin = entry.user
        embed = disnake.Embed(color=disnake.Color.dark_gray(), title = "", description = "")
        embed.set_author(name=guild.name, icon_url=guild.icon.url)
        embed.add_field(name="", value=f'**:family_mmb: Создана роль: {role.mention}**', inline=False)
        embed.add_field(name="**Ответственный модератор:**", value = admin.mention)
        embed.set_footer(text=f"{guild.name} • Дата создания: {datetime.now(tz=self.moscow_tz).strftime('%B %d, %Y %H:%M')}")
        channel = self.bot.get_channel(sinc_channel_id())
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        guild = role.guild
        async for entry in guild.audit_logs(limit=1, action=disnake.AuditLogAction.role_delete):
            admin = entry.user
        embed = disnake.Embed(color=disnake.Color.dark_gray(), title = "", description = "")
        embed.set_author(name=guild.name, icon_url=guild.icon.url)
        embed.add_field(name="", value=f'**:family_mmb: Удалена роль: `{role.name}`**', inline=False)
        embed.add_field(name="**Ответственный модератор:**", value = admin.mention)
        embed.set_footer(text=f"{guild.name} • Дата удаления: {datetime.now(tz=self.moscow_tz).strftime('%B %d, %Y %H:%M')}")
        channel = self.bot.get_channel(sinc_channel_id())
        await channel.send(embed=embed)



    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        guild = after.guild

        async for entry in before.guild.audit_logs(limit=1, action=disnake.AuditLogAction.role_update): 
            admin = entry.user 

        embed = disnake.Embed(color=disnake.Color.dark_gray(), title = "", description = "")
        embed.set_author(name=guild.name, icon_url=guild.icon.url)

        if before.name != after.name:
            embed.add_field(name="", value=f'**:family_mmb: Изменёно название роли роли {after.mention}: `{before.name}` на `{after.name}` **', inline=False)

        if before.color != after.color:
            if before.color.value == 0: old_color = '`Default`'
            else: old_color = before.color
            if after.color.value == 0: new_color = '`Default`'
            else: new_color = after.color
            embed.add_field(name="", value=f'**:family_mmb: Изменён цвет роли {after.mention}: `{old_color}` на `{new_color}` **', inline=False)

        if before.permissions != after.permissions:
            embed.add_field(name='Permissions:', value=f'{after.permissions}', inline=False)
            
        embed.add_field(name="Ответственный модератор:", value = admin.mention)
        embed.set_footer(text=f"{guild.name} • Дата изменения: {datetime.now(tz=self.moscow_tz).strftime('%B %d, %Y %H:%M')}")
        channel = self.bot.get_channel(sinc_channel_id())
        await channel.send(embed=embed)

# Доделать изменение прав ролей

def setup(bot):
    bot.add_cog(RoleLog(bot))