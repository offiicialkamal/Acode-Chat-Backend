import sqlite3

def connect_all_users_table():
    with sqlite3.connect('/DB/all_users.db') as users_database:
        return users_database

    
class create_databasde():
    def __init__(self):
        pass

    def create_users_database(self):
        ###  now i have to crete an unsers database/or going to write his data on all users table 
        with connect_all_users_table() as table:
            cursor = table.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                UID INT,
                FIRST_NAME TEXT,
                LAST_NAME TEXT,
                EMAIL TEXT,
                DOB TEXT,
                PHONE_NO INT,
                IP NUMBER,
                CITY VARCHAR(10),
                PASSWORD TEXT,
                LAST_PW_CHANGED_ON TEXT,
                LAST_LOGIN TEXT,
                TOKEN TEXT,
                COOKIE TEXT
                JOINED_ON TEXT                
            )""")

    def create
            

















    
    
def create_group_messages_database(THREAD_ID):
    try:
        with sqlite3.connect('DBstore/messages.db') as conn:
            cursor = conn.cursor()
            table_name = THREAD_ID + '_' + 'messages'
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
                MESSAGE_ID TEXT,
                SENDER_UID TEXT,
                SENDER_NAME TEXT,
                MESSAGE TEXT,
                TIME TEXT
            )''')
            print(f'Table {table_name} created aucessfully')
            return True
    except Exception as e:
        print(f'erro while creating table {table_name} on messages.db ===> {e}')
        return False

def create_group_database(THREAD_ID):
    try:
        with sqlite3.connect('DBstore/messages.db') as conn:
            cursor = conn.cursor()
            table_name = THREAD_ID + '_' + 'participents'
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
                UID TEXT,
                NAME TEXT
            )'''
            )
            print(f'sucessfully created table {table_name} on messags.db')
            return True
    except Exception as e:
        print(f'error while creating Table {table_name} on message.db ===>>>> {e}')
        return False

def create_users_database():
    try:
        with sqlite3.connect('DBstore/usersDatbase.db') as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users_database (
                    UID TEXT,
                    NAME TEXT,
                    EMAIL TEXT,
                    PH-NO TEXT,
                    DOB TEXT,
                    PASSWORD TEXT,
                    COOKIE TEXT,
                    ACCES_TOKEN TEXT,
                    LAST_PASSWORD_CHANGE_DATE TEXT,
                    JOIN_DATE TEXT,
                    LAST_LOGIN TEXT,
                    IP TEXT
                )''')
            print('susessfully created table users_database on usersDatbase.db')
            return True
    except Exception as e:
        print(f"Error while crreating table users_database on usersDatbase.db =====>>>> {e}")
        return False

def create_users_chat_list_databse(UID):
    try:
        name = UID + "_" + "ChatList"
        with sqlite3.connect('usersChatLists.db') as conn:
            cursor = conn.connect()
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS {name} (
                    THREAD_ID TEXT,
                    NAME TEXT,
                    LAST_UPDATED TEXT,
                    LAST_OPEND TEXT
                )''')
            print(f'sucessfully created Table {name} on usersChatLists.db')
            return True
    except Exception as e:
        print(f"Error while crreating table {name} on usersDatbase.db =====>>>> {e}")
        return False


