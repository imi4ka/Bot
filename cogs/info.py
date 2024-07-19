import disnake
from disnake.ext import commands, tasks
import logging
import os
import asyncio
import sqlite3
from datetime import datetime, timedelta
import pytz
import youtube_dl
import random

class BotInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def list_cogs(self, ctx: commands.Context):
        """Выводит информацию о запущенных когах"""
        cog_list = [cog.qualified_name for cog in self.bot.cogs.values()]
        
        if cog_list:
            embed = disnake.Embed(title="Запущенные коги", color=0x00ff00)
            for cog in cog_list:
                embed.add_field(name=cog, value="", inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Нет загруженных когов.")
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.bot.user.name} has connected to Discord!')


def setup(bot: commands.Bot):
    bot.add_cog(BotInfo(bot))