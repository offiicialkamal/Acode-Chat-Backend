from .connect import database_connection
from .createDatabase import create_database
from datetime import datetime
class write_in_database:
    def add_user(FIRST_NAME, LAST_NAME, EMAIL, IS_MAIL_OTP, DOB, PHONE_NO, IP, CITY,PASSWORD, TOKEN, COOKIE):
        create_database.create_users_database()
        try:
            connection = database_connection.getconn()
            cursor = connection.cursor()
            if cursor:
                cursor.execute("""
                                INSERT INTO users (FIRST_NAME, LAST_NAME, EMAIL, IS_MAIL_OTP, DOB, PHONE_NO, IP, CITY, PASSWORD, TOKEN, COOKIE)
                                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """, 
                            (FIRST_NAME, LAST_NAME, EMAIL, IS_MAIL_OTP, DOB, PHONE_NO, IP, CITY,PASSWORD, TOKEN, COOKIE)
                    )
                connection.commit() # close the connection not cursor
                
                cursor.execute("""
                                SELECT UID FROM users WHERE EMAIL=%s
                                """, (EMAIL,))
                RESULT = cursor.fetchone()
                cursor.close()
               # print(RESULT)
                if RESULT:
                    return RESULT[0]
            else:
                return False
        except Exception as e:
            print(" error on add_user() ",e)
        finally:
            if connection:
                database_connection.putconn(connection)
    
    # ill use it when a user creates a group
    # it will add new group to all chats database
    # and additionally return that new groups uid
    def add_group(GNAME):
        #create table if not exists
        create_database.create_message_list_database()
        try:
            # imsert new group 
            connection = database_connection.getconn()
            cursor = connection.cursor()
            cursor.execute("""
                            INSERT INTO all_chats (GNAME)
                            VALUES(%s)
                            """,(GNAME,))
            cursor.commit()
            
            
            #fetch tbw new group GUID
            cursor.execute("""
                            FROM all_chats SELECT GUID WHERE GNAME= %s
                            """,(GNAME,))
            RESULT = cursor.fetchone()
            cursor.close()
            return RESULT[0] # retur the GUID (imteger)
        except Exception as e:
            print("error  on  add_group(GNAME):",e)
            return False
        finally:
            if connection:
                database_connection.putconn(connection)
    
    # this will add grpup to users table
    # this table will named by each users UID
    # this table will be returned to show all chat list for user
    def add_user_in_group(RAW_UID ,RAW_GUID, GNAME):
        UID = int(RAW_UID)
        GUID = int(RAW_GUID)
        try:
            ## uid is hader or name of create_chats_table_for_this_new_user
            ## GUID is groups uniq id
            ## GNAME is groups name
            create_database.create_chats_table_for_this_new_user(UID)
            create_database.create_chat_database_table(GUID)
            connection = database_connection.getconn()
            cursor = connection.cursor()
            cursor.execute(f"""
                                INSERT INTO CHATS_{str(UID)} (GUID,GNAME)
                                VALUES (%s,%s)
                                ON CONFLICT (GUID) DO NOTHING
                            """, 
                            (GUID, GNAME,))
            connection.commit()
            cursor.close()
        except Exception as e:
            print("error on add_user_in_group(RAW_UID ,RAW_GUID, GNAME):", e)
        finally:
            if connection:
                database_connection.putconn(connection)
    
    # it will store messages
    # each group id represents that specific table
    # this table contains all messages 
    def store_this_message(GROUP_ID, SENDER_ID, SENDER_NAME, MESSAGE):
        create_database.create_chat_database_table(GROUP_ID)
        connection = None
        try:
            connection = database_connection.getconn()
            cursor = connection.cursor()
            cursor.execute(f"""
                    INSERT INTO G_{GROUP_ID} (SENDER_ID, SENDER_NAME, MESSAGE)
                    VALUES(%s, %s, %s)
                    RETURNING MESSAGE_ID, TIME_STAMP
            """, (int(SENDER_ID), SENDER_NAME, MESSAGE))
            # MESSAGE_ID = cursor.lastrowid
            # cursor.execute(f"""
            #                 SELECT TIME_STAMP FROM G_{str(GROUP_ID)} WHERE MESSAGE_ID = %s
            #                 """,(MESSAGE_ID,))
            
            result = cursor.fetchone()
            connection.commit()
            cursor.close()
            return result[0], result[1].isoformat()
        except Exception as e:
            print("error on store_this_message(GROUP_ID, SENDER_ID, SENDER_NAME, MESSAGE):", e)
            return False, False
        finally:
            if connection:
                database_connection.putconn(connection)


