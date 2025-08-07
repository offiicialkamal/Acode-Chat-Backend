import sqlite3
import os
from .connect import connect

class create_database():
    def __init__(self):
        pass

    @staticmethod
    def create_users_database():
        CREDENTIAL_DATABASE_CONNECTED = connect.all_users_table()
        if CREDENTIAL_DATABASE_CONNECTED:
            try:
                cursor = CREDENTIAL_DATABASE_CONNECTED.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                    UID INTEGER PRIMARY KEY AUTOINCREMENT,
                    FIRST_NAME TEXT,
                    LAST_NAME TEXT,
                    EMAIL TEXT,
                    DOB TEXT,
                    PHONE_NO TEXT,
                    IP TEXT,
                    CITY TEXT,
                    PASSWORD TEXT,
                    TOKEN TEXT,
                    COOKIE TEXT,
                    LAST_PW_CHANGED_ON DATETIME DEFAULT CURRENT_TIMESTAMP,
                    LAST_LOGIN DATETIME DEFAULT CURRENT_TIMESTAMP,
                    JOINED_ON DATETIME DEFAULT CURRENT_TIMESTAMP                
                )""")
                CREDENTIAL_DATABASE_CONNECTED.commit()
            except Exception as e:
                print(e)
            finally:
                CREDENTIAL_DATABASE_CONNECTED.close()
        else:
            print('unable to communicate with Credentials database')

    @staticmethod
    def create_chats_table_for_this_new_user(uid):
        CHATS_DATABASE_CONNECTED = connect.user_chats_list_database()
        if CHATS_DATABASE_CONNECTED:
            try:
                cursor = CHATS_DATABASE_CONNECTED.cursor()
                cursor.execute(f"""CREATE TABLE IF NOT EXISTS CHATS_{str(uid)} (
                            S_NO INTEGER PRIMARY KEY AUTOINCREMENT,
                            GUID INTEGER PRIMARY KEY AUTOINCREMENT,
                            GNAME TEXT,
                            TIME_STAMP DATETIME DEFAULT CURRENT_TIMESTAMP
                        )""")
                CHATS_DATABASE_CONNECTED.commit()
            except Exception as e:
                print(e)
                return False
            finally:
                CHATS_DATABASE_CONNECTED.close()
        else:
            print('unable to comunicate with database')

    @staticmethod
    def create_chat_database_table(GROUP_ID, SENDER_ID, SENDER_NAME, MESSAGE):
      #  TABLE_NAME = str(GUID)
        CHAT_DATABASE_CONNECTED = connect.messages_database()
        if CHAT_DATABASE_CONNECTED:
            try:
                cursor = CHAT_DATABASE_CONNECTED.cursor()
                # SID => SENDER ID
                # MID => MESSAGE ID
                # S_NAME => SENDER NAME 
                cursor.execute(f"""CREATE TABLE IF NOT EXISTS G_{str(GROUP_ID)} (
                                    MESSAGE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                                    SENDER_ID INTEGER,
                                    SENDER_NAME TEXT,
                                    MESSAGE TEXT,
                                    TIME_STAMP DATETIME DEFAULT TIME_STAMP                
                                )""")
                CHAT_DATABASE_CONNECTED.commit()
            except Exception as e:
                print(e)
            finally:
                CHAT_DATABASE_CONNECTED.close()
        else:
            print(' unable to comunicate with chat tables database')
            