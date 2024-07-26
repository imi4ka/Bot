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

    def update_members_join_at_user_id(self, joined_at, member_id):
        c = self.connect.cursor()
        c.execute("UPDATE member_join SET joined_at = ? WHERE user_id = ?", (joined_at, member_id))
        self.connect.commit()

    def update_members_left_at(self, left_at, member_id):
        c = self.connect.cursor()
        c.execute("UPDATE member_join SET left_at = ? WHERE user_id = ?", (left_at, member_id))
        self.connect.commit()

    def get_channel_id(self):
        c = self.connect.cursor()
        c.execute("SELECT channel_id FROM settings LIMIT 1")
        return c.fetchone()[0]
    
    def get_user_id_member_join(self, member_id):
        c = self.connect.cursor()
        self.c.execute("SELECT * FROM member_join WHERE user_id = ?", (member_id,))
        return c.fetchone()[0]
    
    def insert_members_join(self, member_id, joined_at):
        c = self.connect.cursor()
        c.execute("INSERT INTO member_join (user_id, joined_at, left_at) VALUES (?, ?, ?)", (member_id, joined_at, ''))
        self.connect.commit()

    def delete_members_member_id(self, member_id):
        c = self.connect.cursor()
        c.execute("DELETE FROM member_join WHERE user_id = ?", (member_id,))
        self.connect.commit()


# db = Db()
# id = db.get_channel_id()
# print(id)



