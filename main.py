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
import sys
from config import token

bot = commands.Bot(command_prefix=">", intents=disnake.Intents.all(), help_command=None, test_guilds = [1260007607222140948])
TOKEN = (token)




def load_extensions(path):
    for filename in os.listdir(path):
        if os.path.isdir(os.path.join(path, filename)):
            load_extensions(os.path.join(path, filename))
        elif filename.endswith('.py') and filename != '__init__.py':
            extension = path.replace('\\', '.') + '.' + filename[:-3]
            try:
                bot.load_extension(extension)
                print(f'Загрузка: {extension}')
            except commands.ExtensionAlreadyLoaded:
                print(f'{extension} Успешно загружены')
            except commands.ExtensionNotFound:
                print(f'{extension} Не найдено')
            except commands.ExtensionFailed:
                print(f'Не удалось загрузить {extension}')

load_extensions('cogs')


bot.run(TOKEN)



