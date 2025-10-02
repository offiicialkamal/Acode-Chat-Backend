from .connect import database
from .createDatabase import create_database
from datetime import datetime
class write_in_database:
    def add_user(FIRST_NAME, LAST_NAME, EMAIL, IS_MAIL_OTP, DOB, PHONE_NO, IP, CITY,PASSWORD, TOKEN, COOKIE, PROFILE_PIC):
        create_database.create_users_database()
        try:
            connection = database.connect_users_db()
            cursor = connection.cursor()
            if cursor:
                cursor.execute("""
                                INSERT INTO users (FIRST_NAME, LAST_NAME, EMAIL, IS_MAIL_OTP, DOB, PHONE_NO, IP, CITY, PASSWORD, TOKEN, COOKIE, PROFILE_PIC)
                                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """, 
                            (FIRST_NAME, LAST_NAME, EMAIL, IS_MAIL_OTP, DOB, PHONE_NO, IP, CITY,PASSWORD, TOKEN, COOKIE, PROFILE_PIC)
                    )
                connection.commit() # close the connection not cursor
                
                cursor.execute("""
                                SELECT UID FROM users WHERE EMAIL=?
                                """, (EMAIL,))
                RESULT = cursor.fetchone()
                cursor.close()
                print(RESULT)
                if RESULT:
                    return RESULT[0]
            else:
                return False
        except Exception as e:
            print(" error on add_user() ",e)
        finally:
            if connection:
                connection.close()
    
    # ill use it when a user creates a group
    # it will add new group to all chats database
    # and additionally return that new groups uid
    def add_group(GNAME, GUID=None):
        #create table if not exists
        create_database.create_message_list_database()
        try:
            # imsert new group 
            connection = database.connect_chat_lists_db()
            cursor = connection.cursor()
            if not GUID:
                cursor.execute("""
                                INSERT INTO all_chats (GNAME)
                                VALUES(?)
                                """,(GNAME,))
            else:
                cursor.execute("""
                                INSERT INTO all_chats (GNAME, GUID)
                                VALUES(?,?)
                                """,(GNAME,GUID))
            connection.commit()
            
            #fetch tbw new group GUID
            cursor.execute("""
                        SELECT GUID FROM all_chats WHERE GNAME= ?
                            """,(GNAME,))
            RESULT = cursor.fetchone()
            cursor.close()
            return RESULT[0] # retur the GUID (imteger)
        except Exception as e:
            print("error  on  add_group(GNAME):",e)
            return False
        finally:
            if connection:
                connection.close()
    
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
            connection = database.connect_chat_lists_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute(f"""
                                    INSERT INTO CHATS_{str(UID)} (GUID,GNAME)
                                    VALUES (?,?)
                                    ON CONFLICT (GUID) DO NOTHING
                                """, 
                                (GUID, GNAME,))
                connection.commit()
                cursor.close()
        except Exception as e:
            print("error on add_user_in_group(RAW_UID ,RAW_GUID, GNAME):", e)
        finally:
            if connection:
                connection.close()
    
    # it will store messages
    # each group id represents that specific table
    # this table contains all messages 
    def store_this_message(GROUP_ID, SENDER_ID, SENDER_NAME, MESSAGE, PROFILE_PIC):
        create_database.create_chat_database_table(GROUP_ID)
        connection = None
        try:
            connection = database.connect_messages()
            cursor = connection.cursor()
            cursor.execute(f"""
                    INSERT INTO G_{GROUP_ID} (SENDER_ID, SENDER_NAME, MESSAGE, PROFILE_PIC)
                    VALUES(?, ?, ?, ?)
            """, (int(SENDER_ID), SENDER_NAME, MESSAGE, PROFILE_PIC))
            connection.commit()
            MESSAGE_ID = cursor.lastrowid
            print(MESSAGE_ID)
            cursor.execute(f"""
                            SELECT TIME_STAMP, PROFILE_PIC FROM G_{str(GROUP_ID)} WHERE MESSAGE_ID = ?
                            """,(MESSAGE_ID,))
            
            result = cursor.fetchone()
            print(result)
            cursor.close()
            return MESSAGE_ID, result[0], result [1] #.isoformat()
        except Exception as e:
            print("error on store_this_message(GROUP_ID, SENDER_ID, SENDER_NAME, MESSAGE):", e)
            return False, False
        finally:
            if connection:
                connection.close()


