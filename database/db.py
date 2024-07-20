import sqlite3


class Db:
    dbname = 'database/bot.db'
    def __init__(self):
        self.connect = sqlite3.connect(self.dbname)
        self.create_tabel_settings()
        self.create_tabel_join()
    def create_tabel_settings(self):
        c = self.connect.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS settings(channel_id TEXT)''')
    def create_tabel_join(self):
        c = self.connect.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS member_join(user_id INTEGER PRIMARY KEY, joined_at TEXT, left_at TEXT)''')
    def update_tabel_settings(self, channel_id):
        c = self.connect.cursor()
        c.execute("UPDATE settings SET channel_id = ?", (channel_id,))
        self.connect.commit()
    def get_channel_id(self):
        c = self.connect.cursor()
        c.execute("SELECT channel_id FROM settings LIMIT 1")
        return c.fetchone()[0]

# db = Db()
# id = db.get_channel_id()
# print(id)



