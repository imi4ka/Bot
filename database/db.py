import sqlite3


class Db:
    dbname = 'database/bot.db'
    def __init__(self):
        self.connect = sqlite3.connect(self.dbname)
        self.create_tabel_settings()
        self.create_tabel_members()
        self.create_tabel_economy()
        self.create_tabel_users_roles()
        self.create_tabel_roles()
        
    def create_tabel_economy(self):
        c = self.connect.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS economy(member_id TEXT, level TEXT, exp TEXT, eternal_role_id TEXT, temporary_role_id TEXT, worker_role_id TEXT)''')

    def create_tabel_roles(self):
        c = self.connect.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS roles(id INTEGER PRIMARY KEY AUTOINCREMENT, role_name TEXT, role_id TEXT, cost TEXT, limit_buying TEXT, description TEXT, reply_message TEXT, role_type TEXT)''')

    def create_tabel_users_roles(self):
        c = self.connect.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users_roles(user_id TEXT, role_id TEXT)''')

    def create_tabel_settings(self):
        c = self.connect.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS settings(channel_id TEXT)''')
        
    def create_tabel_members(self):
        c = self.connect.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS members(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, user_name TEXT, cash TEXT, bank TEXT, joined_at TEXT, left_at TEXT)''')

    def update_tabel_settings(self, channel_id):
        c = self.connect.cursor()
        c.execute("UPDATE settings SET channel_id = ?", (channel_id,))
        self.connect.commit()

    def update_members_join_at_user_id(self, user_name, member_id):
        c = self.connect.cursor()
        c.execute("UPDATE members SET user_name = ?, cash = ?, bank = ? WHERE user_id = ?", (user_name, '0', '0', member_id))
        self.connect.commit()

    def get_channel_id(self):
        c = self.connect.cursor()
        c.execute("SELECT channel_id FROM settings LIMIT 1")
        return c.fetchone()[0]
    
    def get_economy_all_role_id(self):
        c = self.connect.cursor()
        c.execute("SELECT eternal_role_id, temporary_role_id, worker_role_id FROM economy")
        return c.fetchall()

    def get_economy_eternal_role_id(self):
        c = self.connect.cursor()
        c.execute("SELECT eternal_role_id FROM economy")
        return c.fetchall()
    
    def get_economy_temporary_role_id(self):
        c = self.connect.cursor()
        c.execute("SELECT temporary_role_id FROM economy")
        return c.fetchall()
    
    def get_economy_worker_role_id(self):
        c = self.connect.cursor()
        c.execute("SELECT worker_role_id FROM economy")
        return c.fetchall()
    
    def get_all_roles(self):
        c = self.connect.cursor()
        c.execute("SELECT * FROM roles")
        return c.fetchall()
    
    def get_role_by_id(self, role_id):
        c = self.connect.cursor()
        c.execute("SELECT * FROM roles WHERE role_id = ?", (role_id,))
        return c.fetchall()
    
    def get_all_without_roles(self):
        c = self.connect.cursor()
        c.execute("SELECT * FROM roles WHERE role_type IS NULL")
        return c.fetchall()

    def get_all_typed_roles(self, role_type):
        c = self.connect.cursor()
        c.execute("SELECT * FROM roles WHERE role_type = ?", (role_type,))
        return c.fetchall()

    def get_members_ids(self):
        c = self.connect.cursor()
        c.execute('''SELECT * FROM members''')
        return c.fetchall()

    def insert_members_join(self, member_id, member_name):
        c = self.connect.cursor()
        c.execute("INSERT INTO members (user_id, user_name, cash, bank) VALUES (?, ?, ?, ?)", (member_id, member_name, '0', '0'))
        self.connect.commit()

    def insert_typed_role(self, cost, limit_buying, description, reply_message, roles_id):
        c = self.connect.cursor()
        c.execute("INSERT INTO roles (cost, limit_buying, description, reply_message) VALUES (?, ?, ?, ?) WHERE roles_id = ?", (cost, limit_buying, description, reply_message, roles_id,))
        self.connect.commit()

    def insert_type_role(self, role_type, roles_id):
        c = self.connect.cursor()
        c.execute("UPDATE roles SET role_type = ? WHERE role_id = ?", (role_type, roles_id))
        self.connect.commit()  
        
    def insert_role(self, role_name, role_id):
        c = self.connect.cursor()
        c.execute("INSERT INTO roles (role_name, role_id) VALUES (?, ?)", (role_name, role_id))
        self.connect.commit()





db = Db()
# # id = db.get_channel_id()
# # print(id)
# l = db.get_all_roles()
# l.remove(1)
# print(l)

# # if db.get_economy_temporary_role_id() != None:
# #     eternal_list = db.get_temporary_eternal_role_id()
# #     list = [list for list in eternal_list if eternal_list != None]
# # else:
    

# # print(list)
