import sqlite3
import os

class connect:
    # hear all users are stored in a table Called "users"
    def all_users_table():
        try:
            if not os.path.exists('DB'):
                os.makedirs('DB')
            return sqlite3.connect('DB/all_users.db')
        except Exception as e:
            print(f"error accured during connecting to '/DB/all_users.db' ==>>> {e} ")
            return False

    def user_chats_list_database():
        try:
            if not os.path.exists('DB'):
                os.makedirs('DB')
            return sqlite3.connect('DB/chats_list_database.db')
        except Exception as e:
            print(f"error accured while connecting to '/DB/chats_database.db' ==>>>> {e}")
            return False 

    def messages_database():
        try:
            if not os.path.exists('DB'):
                os.makedirs('DB')
            return sqlite3.connect('DB/messages.db')
        except Exception as e:
            print(f"unable to connect '/DB/messages.db' {e}")
            return False
    
    