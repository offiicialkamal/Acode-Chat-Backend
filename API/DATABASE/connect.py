import os
import sqlite3

class database:
        @staticmethod
        def connect_users_db():
                path = 'DB/all_users.db'
                if not os.path.exists('DB'):
                        os.makedirs('DB')
                return sqlite3.connect(path)

        @staticmethod
        def connect_chats_db():
                path = 'DB/chats.db'
                if not os.path.exists('DB'):
                        os.makedirs('DB')
                return sqlite3.connect(path)

        @staticmethod
        def connect_messages():
                path = "DB/messages.db"
                if not os.path.exists('DB'):
                        os.makedirs('DB')
                return sqlite3.connect(path)
                
        def connect_chat_lists_db():
                path = "DB/chats_lists.db"
                if not os.path.exists("DB"):
                        os.makedirs("DB")
                return sqlite3.connect(path)
                
                





# import pymysql
# from dbutils.pooled_db import PooledDB


# database_connection = PooledDB(
#     creator=pymysql,
#     maxconnections=20,
#     mincached=1,
#     maxcached=10,
#     blocking=True,
#     ping=1,
#     host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
#     port=4000,
#     user="2f1tzcw477VuK8y.root",
#     password="3dcvxTbvqoqAOUdJ",
#     database="test",
#     charset="utf8mb4",
#     autocommit=True
# )







# # database_connection = PooledDB(
# #     creator=pymysql,
# #     maxconnections=20,
# #     mincached=1,
# #     maxcached=10,
# #     blocking=True,
# #     ping=1,
# #     host="mysql.db.bot-hosting.net",
# #     port=3306,
# #     user="u463100_TZOZUUiJJA",
# #     password="!c!t^yt8edI7Ki@ksyoob5o.",
# #     database="s463100_Hih",
# #     charset="utf8mb4",
# #     autocommit=True
# # )

# # conn = database_connection.connection()
# # cursor = conn.cursor()
# # cursor.execute("SELECT DATABASE();")
# # print("Connected to DB:", cursor.fetchone()[0])
# # cursor.close()
# # conn.close()







































# # import pg8000
# # import os
# # import psycopg2
# # from psycopg2.pool import ThreadedConnectionPool

# # database_connection = ThreadedConnectionPool(
# #         minconn=1,
# #         maxconn=20,
# #         dsn="postgresql://localhost/mydb"
# #     )




# # def connection():
# #     return pool




# # class connect:
# #     def all_users_table():
# #         return pool.getconn()
    
# #     def user_chats_list_database():
# #         return pool
    
# #     def messages_database():
# #         return pool
    
# #     def message_list_database():
# #         return pool
        
    
    
    
        








# ###### mograted version gives high delay 3-7 seconds
# ###### due to each time connwction

# # DATABASE_URL = 'postgres://hackesofice:npg_0IRsg8YdqaoF@ep-dry-bar-a1zyxhba.ap-southeast-1.pg.koyeb.app/koyebdb'
# # class connect:
# #     # hear all users are stored in a table Called "users"
# #     def all_users_table():
# #         try:
# #             if not os.path.exists('DB'):
# #                 os.makedirs('DB')
# #             # return pg8000.connect(
# #             #     user="offiicialkamal",
# #             #     password="xbfaCQ8x9NLFEOQzBloQgEKXB41ge5G0",
# #             #     host="dpg-d2jb0op5pdvs73f0uqvg-a.frankfurt-postgres.render.com",
# #             #     port=5432,
# #             #     database="acode_chat_backend"
# #             # )
# #             return psycopg2.connect(DATABASE_URL)
# #         except Exception as e:
# #             print(f"error accured during connecting to '/DB/all_users.db' ==>>> {e} ")
# #             return False

# #     def user_chats_list_database():
# #         try:
# #             if not os.path.exists('DB'):
# #                 os.makedirs('DB')
# #             # return pg8000.connect(
# #             #     user="offiicialkamal",
# #             #     password="xbfaCQ8x9NLFEOQzBloQgEKXB41ge5G0",
# #             #     host="dpg-d2jb0op5pdvs73f0uqvg-a.frankfurt-postgres.render.com",
# #             #     port=5432,
# #             #     database="acode_chat_backend"
# #             # )
# #             return psycopg2.connect(DATABASE_URL)
# #         except Exception as e:
# #             print(f"error accured while connecting to '/DB/chats_database.db' ==>>>> {e}")
# #             return False 

# #     def messages_database():
# #         try:
# #             if not os.path.exists('DB'):
# #                 os.makedirs('DB')
# #             # return pg8000.connect(
# #             #     user="offiicialkamal",
# #             #     password="xbfaCQ8x9NLFEOQzBloQgEKXB41ge5G0",
# #             #     host="dpg-d2jb0op5pdvs73f0uqvg-a.frankfurt-postgres.render.com",
# #             #     port=5432,
# #             #     database="acode_chat_backend"
# #             # )
# #             return psycopg2.connect(DATABASE_URL)
# #         except Exception as e:
# #             print(f"unable to connect '/DB/messages.db' {e}")
# #             return False
    
# #     def message_list_database():
# #         try:
# #             if not os.path.exists('DB'):
# #                 os.makedirs('DB')
# #             # return pg8000.connect(
# #             #     user="offiicialkamal",
# #             #     password="xbfaCQ8x9NLFEOQzBloQgEKXB41ge5G0",
# #             #     host="dpg-d2jb0op5pdvs73f0uqvg-a.frankfurt-postgres.render.com",
# #             #     port=5432,
# #             #     database="acode_chat_backend"
# #             # )
# #         except Exception as e:
# #             return psycopg2.connect(DATABASE_URL)
# #             print(e)
# #             return False
    
    