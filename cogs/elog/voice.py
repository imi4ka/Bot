import disnake
from disnake.ext import commands
from datetime import datetime
import pytz

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    moscow_tz = pytz.timezone('Europe/Moscow')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        guild = after.guild
        embed = disnake.Embed(color=disnake.Color.dark_gray())
        embed.set_author(name=member.name, icon_url=member.display_avatar.url)
        if before.channel is None and after.channel is not None:
            embed.add_field(name="", value=f"**{member.mention} подключился к каналу `{after.channel.name}`**", inline=False)
        elif before.channel is not None and after.channel is None:
            embed.add_field(name="", value=f"**{member.mention} Отключился от канала `{before.channel.name}`**", inline=False)
        elif  before.channel != after.channel:
            embed.add_field(name = '', value = f'**{member.mention} Сменил голосовой канал c `{before.channel.name}` на `{after.channel.name}`**', inline = False)
        embed.set_footer(text=f"{guild.name} • Дата отключения: {datetime.now(tz=self.moscow_tz).strftime('%B %d, %Y %H:%M')}")
        await disnake.utils.get(member.guild.text_channels, id=1262100877066633267).send(embed=embed)



def setup(bot):
    bot.add_cog(Voice(bot))