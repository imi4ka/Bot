import disnake
from disnake.ext import commands
from datetime import datetime
import pytz
import sqlite3


class Tlogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    moscow_tz = pytz.timezone('Europe/Moscow')



    log_folder = "logs"
    current_log_date = None
    current_log_file = None

    async def log_message(self, message, event_type):
        global current_log_date
        global current_log_file
        current_date = datetime.now().strftime("%Y-%m-%d")
        if current_log_date != current_date:
            current_log_date = current_date
            current_log_file = self.setup_logging(current_date)


        channel_info = f'Channel: {message.channel.name} ({message.channel.id})'
        user_info = f'User: {message.author}'
        message_content = f'Message: {message.content}'

        if event_type == 'message':
            self.logging.info(f'[Message] {channel_info} | {user_info}: {message_content}')
        elif event_type == 'edit':
            self.logging.info(
                f'[Message Edit] {channel_info} | {user_info}: {message_content} (before: {message.content}, after: {message.content})')
        elif event_type == 'delete':
            self.logging.info(f'[Message Delete] {channel_info} | {user_info}: {message_content}')


    def check_log_file(self):
        global current_log_date
        current_date = datetime.now().strftime("%Y-%m-%d")
        if current_log_date != current_date:
            current_log_date = current_date
            global current_log_file
            current_log_file = self.setup_logging(current_date)


    async def log_checker(self):
        while True:
            self.check_log_file()
            await self.asyncio.sleep(3600)  # Задержка на 1 час (в секундах)


    @commands.Cog.listener()
    async def on_message(self,message):
        if not message.author.bot:
            await self.log_message(message, 'message')
        await self.bot.process_commands(message)


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not after.author.bot:
            await self.log_message(after, 'edit')


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            await self.log_message(message, 'delete')
        await self.bot.process_commands(message)


    def setup_logging(current_date, self):
        log_folder_path = self.os.path.join(self.log_folder, current_date)
        self.os.makedirs(log_folder_path, exist_ok=True)
        log_filename = self.os.path.join(log_folder_path, f'{current_date}.log')
        self.logging.basicConfig(filename=log_filename, level=self.logging.INFO, format='%(asctime)s | %(levelname)s: %(message)s')
        return log_filename


    def start_checker(self):
        self.bot.loop.create_task(self.log_checker())



def setup(bot):
    bot.add_cog(Tlogs(bot))