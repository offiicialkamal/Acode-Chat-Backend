# import pg8000
import os
import psycopg2
from psycopg2.pool import ThreadedConnectionPool

database_connection = ThreadedConnectionPool(
        minconn=1,
        maxconn=20,
        dsn="postgresql://localhost/mydb"
    )




# def connection():
#     return pool




# class connect:
#     def all_users_table():
#         return pool.getconn()
    
#     def user_chats_list_database():
#         return pool
    
#     def messages_database():
#         return pool
    
#     def message_list_database():
#         return pool
        
    
    
    
        








###### mograted version gives high delay 3-7 seconds
###### due to each time connwction

# DATABASE_URL = 'postgres://hackesofice:npg_0IRsg8YdqaoF@ep-dry-bar-a1zyxhba.ap-southeast-1.pg.koyeb.app/koyebdb'
# class connect:
#     # hear all users are stored in a table Called "users"
#     def all_users_table():
#         try:
#             if not os.path.exists('DB'):
#                 os.makedirs('DB')
#             # return pg8000.connect(
#             #     user="offiicialkamal",
#             #     password="xbfaCQ8x9NLFEOQzBloQgEKXB41ge5G0",
#             #     host="dpg-d2jb0op5pdvs73f0uqvg-a.frankfurt-postgres.render.com",
#             #     port=5432,
#             #     database="acode_chat_backend"
#             # )
#             return psycopg2.connect(DATABASE_URL)
#         except Exception as e:
#             print(f"error accured during connecting to '/DB/all_users.db' ==>>> {e} ")
#             return False

#     def user_chats_list_database():
#         try:
#             if not os.path.exists('DB'):
#                 os.makedirs('DB')
#             # return pg8000.connect(
#             #     user="offiicialkamal",
#             #     password="xbfaCQ8x9NLFEOQzBloQgEKXB41ge5G0",
#             #     host="dpg-d2jb0op5pdvs73f0uqvg-a.frankfurt-postgres.render.com",
#             #     port=5432,
#             #     database="acode_chat_backend"
#             # )
#             return psycopg2.connect(DATABASE_URL)
#         except Exception as e:
#             print(f"error accured while connecting to '/DB/chats_database.db' ==>>>> {e}")
#             return False 

#     def messages_database():
#         try:
#             if not os.path.exists('DB'):
#                 os.makedirs('DB')
#             # return pg8000.connect(
#             #     user="offiicialkamal",
#             #     password="xbfaCQ8x9NLFEOQzBloQgEKXB41ge5G0",
#             #     host="dpg-d2jb0op5pdvs73f0uqvg-a.frankfurt-postgres.render.com",
#             #     port=5432,
#             #     database="acode_chat_backend"
#             # )
#             return psycopg2.connect(DATABASE_URL)
#         except Exception as e:
#             print(f"unable to connect '/DB/messages.db' {e}")
#             return False
    
#     def message_list_database():
#         try:
#             if not os.path.exists('DB'):
#                 os.makedirs('DB')
#             # return pg8000.connect(
#             #     user="offiicialkamal",
#             #     password="xbfaCQ8x9NLFEOQzBloQgEKXB41ge5G0",
#             #     host="dpg-d2jb0op5pdvs73f0uqvg-a.frankfurt-postgres.render.com",
#             #     port=5432,
#             #     database="acode_chat_backend"
#             # )
#         except Exception as e:
#             return psycopg2.connect(DATABASE_URL)
#             print(e)
#             return False
    
    