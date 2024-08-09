import disnake
from disnake.ext import commands
from datetime import datetime
import pytz
from database.db import Db
db = Db()

def sinc_channel_id():
    channel_id = int(db.get_channel_id())
    return channel_id

class Join_Diss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    moscow_tz = pytz.timezone('Europe/Moscow')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        joined_at = member.joined_at.astimezone(self.moscow_tz).strftime('%Y-%m-%d %H:%M:%S')
        member_id = [ids[1] for ids in db.get_members_ids()]
        if str(member.id) in member_id:
            db.update_members_join_at_user_id(member.name, member.id)
        else:
            db.insert_members_join(member.id, member.name)
        embed = disnake.Embed(color=disnake.Color.dark_gray(), title="", description=f"{member.mention} присоединился к серверу.")
        embed.set_author(name=member.name, icon_url=member.display_avatar.url)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Дата регистрации аккаунта", value=f"{member.created_at.astimezone(self.moscow_tz).strftime('%Y/%m/%d %H:%M:%S')}", inline=False)
        embed.add_field(name="", value=f"{(datetime.now(tz=self.moscow_tz) - member.created_at.astimezone(self.moscow_tz)).days // 365} лет назад", inline=False)
        embed.set_footer(text=f"{guild.name} • Дата выхода: {datetime.now(tz=self.moscow_tz).strftime('%B %d, %Y %H:%M')}")
        channel = self.bot.get_channel(sinc_channel_id())
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        moscow_tz = pytz.timezone('Europe/Moscow')
        left_at = datetime.now(tz=moscow_tz).strftime('%Y-%m-%d %H:%M:%S')
        guild = member.guild
        joined_at = member.joined_at.astimezone(self.moscow_tz).strftime('%Y-%m-%d %H:%M:%S')
        joined_at_dt = datetime.strptime(joined_at, '%Y-%m-%d %H:%M:%S').replace(tzinfo=moscow_tz)
        left_at_dt = datetime.strptime(left_at, '%Y-%m-%d %H:%M:%S').replace(tzinfo=moscow_tz)
        time_on_server = left_at_dt - joined_at_dt
        days_on_server = time_on_server.days
        hours_on_server = time_on_server.seconds // 3600
        minutes_on_server = (time_on_server.seconds // 60) % 60
        seconds_on_server = time_on_server.seconds % 60
        embed = disnake.Embed(color=disnake.Color.dark_gray(), title="", description=f"{member.mention} покинул сервер.")
        embed.set_author(name=member.name, icon_url=member.display_avatar.url)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name="Дата вступления на сервер", value=f"{joined_at}", inline=False)
        embed.add_field(name="Время, проведенное на сервере:", value=f"{days_on_server} дней, {hours_on_server} часов, {minutes_on_server} минут, {seconds_on_server} секунд", inline=False)
        embed.set_footer(text=f"{guild.name} • Дата выхода: {datetime.now(tz=moscow_tz).strftime('%B %d, %Y %H:%M')}")
        channel = self.bot.get_channel(sinc_channel_id())
        await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_invite_create(self, invite: disnake.Invite):
        guild = invite.guild
        async for entry in guild.audit_logs(limit=1, action=disnake.AuditLogAction.invite_create):
            creator = entry.user
        embed = disnake.Embed(color = disnake.Color.dark_gray(), title = '', description = '')
        embed.set_author(name = guild.name, icon_url = guild.icon.url)
        embed.add_field(name = '', value = f'{creator.mention} **Создал ссылку приглашения на сервер.**', inline = False)
        if invite.max_uses == 0:
            max_uses = 'Безграничное'
        else:
            max_uses = invite.max_uses
        embed.add_field(name = '', value = f'**Максимальное кол-во использований:** `{max_uses}`', inline = False)
        embed.add_field(name = '', value = f'**Работающее время ссылки:** `{(invite.max_age // 60) / 60} часов`', inline = False)
        embed.add_field(name = '', value = f'**Код ссылки:** `{invite.id}`', inline = False)
        embed.add_field(name = '', value = f'[Ссылка]({invite.url})')
        embed.set_footer(text = f'{guild.name} • Дата выхода: {datetime.now(tz=self.moscow_tz).strftime('%B %d, %Y %H:%M')}')
        channel = self.bot.get_channel(sinc_channel_id())
        await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_invite_delete(self, invite: disnake.invite):
        guild = invite.guild
        async for entry in guild.audit_logs(limit=1, action=disnake.AuditLogAction.invite_create):
            creator = entry.user
        embed = disnake.Embed(color = disnake.Color.dark_gray(), title = '', description = '')
        embed.set_author(name = guild.name, icon_url = guild.icon.url)
        embed.add_field(name = '', value = f'{creator.mention} **Удалил ссылку приглашения на сервер.**', inline = False)
        embed.add_field(name = '', value = f'**Код ссылки:** `{invite.id}`', inline = False)
        embed.set_footer(text = f'{guild.name} • Дата выхода: {datetime.now(tz=self.moscow_tz).strftime('%B %d, %Y %H:%M')}')
        channel = self.bot.get_channel(sinc_channel_id())
        await channel.send(embed=embed)

        


def setup(bot):
    bot.add_cog(Join_Diss(bot))