import sqlite3
import os
from .connect import database_connection

class create_database():
    def __init__(self):
        pass
    
    @staticmethod
    def create_users_database():
        CREDENTIAL_DATABASE_CONNECTED = database_connection.getconn()
        if CREDENTIAL_DATABASE_CONNECTED:
            try:
                cursor = CREDENTIAL_DATABASE_CONNECTED.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                    UID BIGSERIAL PRIMARY KEY,
                    FIRST_NAME TEXT,
                    LAST_NAME TEXT,
                    EMAIL TEXT,
                    IS_MAIL_OTP INTEGER,
                    DOB TEXT,
                    PHONE_NO TEXT,
                    IP TEXT,
                    CITY TEXT,
                    PASSWORD TEXT,
                    TOKEN TEXT,
                    COOKIE TEXT,
                    LAST_PW_CHANGED_ON TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    LAST_LOGIN TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    JOINED_ON TIMESTAMP DEFAULT CURRENT_TIMESTAMP                
                )""")
                CREDENTIAL_DATABASE_CONNECTED.commit()
                cursor.close()
                return True
            except Exception as e:
                print("error on create_users_database():",e)
                return False
            finally:
                if CREDENTIAL_DATABASE_CONNECTED:
                    database_connection.putconn(CREDENTIAL_DATABASE_CONNECTED)
        else:
            print('unable to communicate with Credentials database')

    @staticmethod
    def create_chats_table_for_this_new_user(RAW_UID):
        UID = str(RAW_UID)
        CHATS_DATABASE_CONNECTED = database_connection.getconn()
        if CHATS_DATABASE_CONNECTED:
            try:
                cursor = CHATS_DATABASE_CONNECTED.cursor()
                cursor.execute(f"""CREATE TABLE IF NOT EXISTS CHATS_{str(UID)} (
                            GUID BIGSERIAL PRIMARY KEY,
                            GNAME TEXT,
                            TIME_STAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )""")
                CHATS_DATABASE_CONNECTED.commit()
                cursor.close()
                return True
            except Exception as e:
                print("error on create_chats_table_for_this_new_user(RAW_UID):",e)
                return False
            finally:
                if CHATS_DATABASE_CONNECTED:
                    database_connection.putconn(CHATS_DATABASE_CONNECTED)
        else:
            print('unable to comunicate with database')

    @staticmethod
    def create_chat_database_table(GROUP_ID):
      #  TABLE_NAME = str(GUID)
        CHAT_DATABASE_CONNECTED = database_connection.getconn()
        if CHAT_DATABASE_CONNECTED:
            try:
                cursor = CHAT_DATABASE_CONNECTED.cursor()
                # SID => SENDER ID
                # MID => MESSAGE ID
                # S_NAME => SENDER NAME
                cursor.execute(f"""CREATE TABLE IF NOT EXISTS G_{str(GROUP_ID)} (
                                    MESSAGE_ID BIGSERIAL PRIMARY KEY,
                                    SENDER_ID INTEGER,
                                    SENDER_NAME TEXT,
                                    MESSAGE TEXT,
                                    TIME_STAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP               
                                )""")
                CHAT_DATABASE_CONNECTED.commit()
                cursor.close()
                return True
            except Exception as e:
                print("error on create_chat_database_table(GROUP_ID):", e)
                return False
            finally:
                if CHAT_DATABASE_CONNECTED:
                    database_connection.putconn(CHAT_DATABASE_CONNECTED)
        else:
            print(' unable to comunicate with chat tables database')
    
    @staticmethod
    def create_message_list_database():
        try:
            connection = database_connection.getconn()
            if  connection:
                cursor = connection.cursor()
                cursor.execute("""
                                CREATE TABLE IF NOT EXISTS all_chats (
                                    GUID BIGSERIAL PRIMARY KEY,
                                    GNAME TEXT,
                                    TIME_STAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                )
                                """)
                connection.commit()
                cursor.close()
                return True
        except Exception as e:
            print("error on create_message_list_database()  :", e)
            return False
        finally:
            if connection:
                database_connection.putconn(connection)
    
        
