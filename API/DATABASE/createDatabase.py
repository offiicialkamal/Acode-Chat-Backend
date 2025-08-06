import sqlite3
import os



def connect_all_users_table():
    try:
        if not os.path.exists('DB'):
            os.makedirs('DB')
                              
        return sqlite3.connect('DB/all_users.db')
        #with sqlite3.connect('DB/all_users.db') as users_database:
         #   return users_database
    except Exception as e:
        print(f"error accured during connecting to '/DB/all_users.db' ==>>> {e} ")
        return False

# def connect_user_chats_list_database():
#     try:
#         with sqlite3.connect('DB/chats_list_database.db') as chats_database:
#             return chats_database
#     except Exception as e:
#         print(f"error accured while connecting to '/DB/chats_database.db' ==>>>> {e}")
#         return False 

# def connect_chats_tabes_database():
#     try:
#         with sqlite3.connect('/DB/chats_tables.db') as chat_database:
#             return chat_database
#     except Exception as e:
#         print(f"unable to connect '/DB/chat.db' {e}")
#         return False
    
class create_database():
    def __init__(self):
        pass

    @staticmethod
    def create_users_database():
        ###  now i have to crete an unsers database/or going to write his data on all users table 
        CREDENTIAL_DATABASE_CONNECTED = connect_all_users_table()
        if CREDENTIAL_DATABASE_CONNECTED:
            # with CREDENTIAL_DATABASE_CONNECTED as table:
                # cursor = table.cursor()
            try:
                cursor = CREDENTIAL_DATABASE_CONNECTED.cursor()
                cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                    UID TEXT,
                    FIRST_NAME TEXT,
                    LAST_NAME TEXT,
                    EMAIL TEXT,
                    DOB TEXT,
                    PHONE_NO TEXT,
                    IP TEXT,
                    CITY TEXT,
                    PASSWORD TEXT,
                    LAST_PW_CHANGED_ON TEXT,
                    LAST_LOGIN TEXT,
                    TOKEN TEXT,
                    COOKIE TEXT,
                    JOINED_ON TEXT                
                )""")
                CREDENTIAL_DATABASE_CONNECTED.commit()
            except Exception as e:
                print(e)
            finally:
                CREDENTIAL_DATABASE_CONNECTED.close()

        else:
            print('unable to communicate with Credentials database')
        # finally:
        #     CREDENTIAL_DATABASE_CONNECTED.close()
#     @staticmethod
#     def create_chats_table_for_this_new_user():
#         CHATS_DATABASE_CONNECTED = connect_user_chats_list_database()
#         if CHATS_DATABASE_CONNECTED:
#             with CHATS_DATABASE_CONNECTED as table:
#                 cursor = table.cursor()
#                 cursor.execute("""CREATE TABLE IF NOT EXISTS uid (
#                                 S_NO NUMBER,
#                                 GUID NUMBER,
#                                 GNAME TEXT
#                             )""")
#         else:
#             print('unable to comunicate with database')

#     @staticmethod
#     def crete_chat_database_table():
#         CHAT_DATABASE_CONNECTED = connect_chats_tables_database()
#         if CHAT_DATABASE_CONNECTED:
#             with CHAT_DATABASE_CONNECTED as chats:
#                 cursor = chats.cursor()
#                 # SID => SENDER ID
#                 # MID => MESSAGE ID
#                 # S_NAME => SENDER NAME 
#                 cursor.execute("""CREATE TABLE IF NOT EXISTS guid (
#                                     MID NUMBER,
#                                     SID NUMBER,
#                                     SENDER_NAME TEXT,
#                                     MESSAGE TEXT,
#                                     TIME_STAMP DEFAULT CURRENT_TIMESTAMP                
#                                 )""")
#         else:
#             print(' unable to comunicate with chat tables database')
            

















    
    
# def create_group_messages_database(THREAD_ID):
#     try:
#         with sqlite3.connect('DBstore/messages.db') as conn:
#             cursor = conn.cursor()
#             table_name = THREAD_ID + '_' + 'messages'
#             cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
#                 MESSAGE_ID TEXT,
#                 SENDER_UID TEXT,
#                 SENDER_NAME TEXT,
#                 MESSAGE TEXT,
#                 TIME TEXT
#             )''')
#             print(f'Table {table_name} created aucessfully')
#             return True
#     except Exception as e:
#         print(f'erro while creating table {table_name} on messages.db ===> {e}')
#         return False

# def create_group_database(THREAD_ID):
#     try:
#         with sqlite3.connect('DBstore/messages.db') as conn:
#             cursor = conn.cursor()
#             table_name = THREAD_ID + '_' + 'participents'
#             cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
#                 UID TEXT,
#                 NAME TEXT
#             )'''
#             )
#             print(f'sucessfully created table {table_name} on messags.db')
#             return True
#     except Exception as e:
#         print(f'error while creating Table {table_name} on message.db ===>>>> {e}')
#         return False

# def create_users_database():
#     try:
#         with sqlite3.connect('DBstore/usersDatbase.db') as conn:
#             cursor = conn.cursor()
#             cursor.execute('''CREATE TABLE IF NOT EXISTS users_database (
#                     UID TEXT,
#                     NAME TEXT,
#                     EMAIL TEXT,
#                     PH-NO TEXT,
#                     DOB TEXT,
#                     PASSWORD TEXT,
#                     COOKIE TEXT,
#                     ACCES_TOKEN TEXT,
#                     LAST_PASSWORD_CHANGE_DATE TEXT,
#                     JOIN_DATE TEXT,
#                     LAST_LOGIN TEXT,
#                     IP TEXT
#                 )''')
#             print('susessfully created table users_database on usersDatbase.db')
#             return True
#     except Exception as e:
#         print(f"Error while crreating table users_database on usersDatbase.db =====>>>> {e}")
#         return False

# def create_users_chat_list_databse(UID):
#     try:
#         name = UID + "_" + "ChatList"
#         with sqlite3.connect('usersChatLists.db') as conn:
#             cursor = conn.connect()
#             cursor.execute(f'''CREATE TABLE IF NOT EXISTS {name} (
#                     THREAD_ID TEXT,
#                     NAME TEXT,
#                     LAST_UPDATED TEXT,
#                     LAST_OPEND TEXT
#                 )''')
#             print(f'sucessfully created Table {name} on usersChatLists.db')
#             return True
#     except Exception as e:
#         print(f"Error while crreating table {name} on usersDatbase.db =====>>>> {e}")
#         return False


