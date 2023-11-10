import sqlite3

class User:

    def __init__(self) :
        self.conn = sqlite3.connect('bot.sqlite' , check_same_thread=False)
        self.cursor = self.conn.cursor()

    def adding_user(self ,chat_id:int , is_admin:str , user_name:str , first_name:str):
        self.cursor.execute('INSERT INTO users (chat_id, username, is_admin, firs_name ) VALUES (?, ?, ?, ?)', (chat_id , user_name , is_admin , first_name))
        self.conn.commit()
    def check_user_into_database(self , chat_id:int):
        self.cursor.execute('SELECT * from users')
        records = self.cursor.fetchall()
        for row in records:
            if row[1] == chat_id :
                return False
        return True
    def get_all_users(self):
        self.cursor.execute('SELECT * from users')
        records = self.cursor.fetchall()
        return records

class Chanals:
    def __init__(self):
        self.conn = sqlite3.connect('bot.sqlite' , check_same_thread=False)
        self.cursor = self.conn.cursor()
    def get_all_chanals(self):
        self.cursor.execute('SELECT * from chanals')
        records = self.cursor.fetchall()
        return records
    def create_chanal(self, chanal_name:str):
        self.cursor.execute('INSERT INTO chanals (chanal_name) VALUES(?)' , [chanal_name])
        self.conn.commit()
    def delete_chanal(self, chanal_id:int):
        query = 'DELETE FROM chanals WHERE id = ' + str(chanal_id)
        self.cursor.execute(query)
        self.conn.commit()
