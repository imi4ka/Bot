import disnake
from disnake.ext import commands
from datetime import datetime
import pytz

class CommandsB(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    moscow_tz = pytz.timezone('Europe/Moscow')

    @commands.slash_command(name = 'бан', description = 'Команда для блокировки участников сервера')
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx: disnake.ApplicationCommandInteraction, member: disnake.Member, reason = None):
        global guild
        guild = ctx.guild
        embed = disnake.Embed(color=disnake.Color.dark_grey())
        embed.set_author(name=guild.name, icon_url=guild.icon.url)
        embed.set_thumbnail(url=member.display_avatar.url)
        if reason == None:
            reason = 'Без причины'
        embed.add_field(name = '', value = f'Пользователь {member.mention} был забанен модератором {ctx.author.mention} по причине `{reason}`.')
        embed.set_footer(text=f"{guild.name} • Дата выхода: {datetime.now(tz=self.moscow_tz).strftime('%B %d, %Y %H:%M')}")
        await ctx.send(embed = embed)
        await member.ban

    @commands.slash_command(name = 'разбан', description = 'Команда для разблокировки участников сервера')
    @commands.has_permissions(ban_members = True)
    async def unban(self, ctx: disnake.ApplicationCommandInteraction, member: disnake.Member):
        embed = disnake.Embed(color=disnake.Color.dark_grey())
        embed.set_author(name=guild.name, icon_url=guild.icon.url)
        embed.set_thumbnail(url=member.display_avatar.url)
        if reason == None:
            reason = 'Без причины'
        embed.add_field(name = '', value = f'Пользователь {member.mention} был забанен модератором {ctx.author.mention} по причине `{reason}`.')
        embed.set_footer(text=f"{guild.name} • Дата выхода: {datetime.now(tz=self.moscow_tz).strftime('%B %d, %Y %H:%M')}")
        await ctx.send(embed = embed)
        await member.unban

    @commands.slash_command(name = 'мут', description = 'Команда для мута участников сервера')
    @commands.has_permissions()
    async def mute(self, ctx, member: disnake.Member, reason = None):
        mrole = disnake.utils.get(guild.roles, name = 'Muted')
        if not mrole:
            mrole = await guild.create_role(name = 'Muted')
        for channel in guild.channels:
            await channel.set_permissions(mrole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
        if reason == None:
            reason = 'Без причины'
        embed = disnake.Embed(color=disnake.Color.dark_grey())
        embed.set_author(name=guild.name, icon_url=guild.icon.url)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name = '', value = f'Пользователь {member.mention} был замучен модератором {ctx.author.mention} по причине `{reason}`.')
        embed.set_footer(text=f"{guild.name} • Дата выхода: {datetime.now(tz=self.moscow_tz).strftime('%B %d, %Y %H:%M')}")
        await ctx.send(embed = embed)
        await member.add_roles(mrole, reason = reason)


    @commands.slash_command(name = 'размут', description = 'Команда для размута участников сервера')
    @commands.has_permissions()
    async def unmute(self, ctx: disnake.ApplicationCommandInteraction, member: disnake.Member):
        mrole = disnake.utils.get(guild.roles, name = 'Muted')
        embed = disnake.Embed(color = disnake.Color.dark_grey())
        embed.set_author(name = guild.name, icon_url = guild.icon.url)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name = '', value = f'Пользователь {member.mention} был размучен модератором {ctx.author.mention}.')
        embed.set_footer(text=f"{guild.name} • Дата выхода: {datetime.now(tz=self.moscow_tz).strftime('%B %d, %Y %H:%M')}")
        await ctx.send(embed = embed)
        await member.remove_roles(mrole)

    @commands.slash_command(name = 'таймаут', description = 'Команда для таймаута участников сервера')
    @commands.has_permissions(manage_roles = True)
    async def timeout(self, ctx: disnake.ApplicationCommandInteraction, member: disnake.Member, reason = None, duration = None):
        guild = ctx.guild
        embed = disnake.Embed(color = disnake.Color.dark_gray)
        embed.set_author(name = guild.name, icon_url = guild.icon.url)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"{guild.name} • Дата выхода: {datetime.now(tz=self.moscow_tz).strftime('%B %d, %Y %H:%M')}")
        if reason == None:
            reason = 'Без причины'
        if duration == None:
            embed.add_field(name = 'Ошибка😡', value = 'Введите время тайм-аута.')
            await ctx.send(embed = embed)
        if duration != None:
            embed.add_field(name = '', value = f'Пользователь {member.mention} отправлен в тайм аут на {duration} модератором {ctx.author.mention}')
            await ctx.send(embed = embed)
            await member.timeout(duration = duration, reason = reason)

    @commands.slash_command(name = 'кик', description = 'Команда для исключения участника с сервера')
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: disnake.Member, reason = None):
        embed = disnake.Embed(color = disnake.Color.dark_gray)
        embed.set_author(name = guild.name, icon_url = guild.icon.url)
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.add_field(name = '', value = f'Пользователь {member.mention} был кикнут с сервера модератором {ctx.author.mention}.')
        await ctx.send(embed = embed)
        await member.kick
    
def setup(bot: commands.Bot):
    bot.add_cog(CommandsB(bot))