import sqlite3

class database:
    def __init__(self):
        print(self)

    @classmethod
    def connect_database(self, database_name):
        with sqlite3.connect(f"DB/{FILE_NAME}") as data:
            cursor = data.cursor()
            cursor.ececute('''SELECT UID FROM''')


        
    def provide_cookie(self):
        print("cookies sent")