import disnake
from disnake.ext import commands
from datetime import datetime
import pytz
from database.db import Db
db = Db()
global channel_id
channel_id = int(db.get_channel_id())


class Banwords(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    moscow_tz = pytz.timezone('Europe/Moscow')


    def read_file():
        with open('file/ban_words.txt', 'r', encoding='utf-8') as file:
            text = file.read()
            words = text.split()
            ban_words = words.copy()
            return ban_words

    def simplify_word(word):
        last_letter = ''
        result = ''
        for letter in word:
            if letter != last_letter:
                last_letter = letter
                result += letter

        return result

    def lower(word):
        return word.lower()


    ban_words = read_file()
    required_roles = ['новая роль', '2']
    allowed_channels = ['тест', '123']
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:  # зависимость от сообщения от бота
            return
        member_roles = [role.name for role in message.author.roles]
        msg_words = [self.simplify_word(word.lower()) for word in message.content.split()]
        for word in msg_words:
            if word.lower() in self.ban_words and any(role_name in member_roles for role_name in self.required_roles) and message.channel.name in self.allowed_channels:
                try:
                    await message.delete()
                except:
                    print('Ошибка при удалении сообщения')
                emb = disnake.Embed(
                    title="Нарушение",
                    description="Матершиник найден",
                    timestamp=message.created_at,
                    color=disnake.Color.blue())
                emb.add_field(name='Канал:', value=message.channel.mention, inline=True)
                emb.add_field(name='Нарушитель:', value=message.author.mention, inline=True)
                emb.add_field(name='Тип:', value='Мат/Оскорбление/Травля см. содержание', inline=True)
                emb.add_field(name='Содержимое:', value=message.content, inline=True)
                channel = self.bot.get_channel(channel_id)
                await channel.send(embed=emb)
                return


def setup(bot):
    bot.add_cog(Banwords(bot))