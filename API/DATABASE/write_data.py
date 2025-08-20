from .connect import connect
from .createDatabase import create_database

class write_in_database:
    def add_user(FIRST_NAME, LAST_NAME, EMAIL, IS_MAIL_OTP, DOB, PHONE_NO, IP, CITY,PASSWORD, TOKEN, COOKIE):
        create_database.create_users_database()
        try:
            connection = connect.all_users_table()
            cursor = connection.cursor()
            if cursor:
                cursor.execute("""
                                INSERT INTO users (FIRST_NAME, LAST_NAME, EMAIL, IS_MAIL_OTP, DOB, PHONE_NO, IP, CITY, PASSWORD, TOKEN, COOKIE)
                                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """, 
                            (FIRST_NAME, LAST_NAME, EMAIL, IS_MAIL_OTP, DOB, PHONE_NO, IP, CITY,PASSWORD, TOKEN, COOKIE)
                    )
                connection.commit() # close the connection not cursor
                
                cursor.execute("""
                                SELECT UID FROM users WHERE EMAIL=?
                                """, (EMAIL,))
                RESULT = cursor.fetchone()
               # print(RESULT)
                if RESULT:
                    return RESULT[0]
            else:
                return False
        except Exception as e:
            print(e)
        finally:
            connection.close()
    
    # ill use it when a user creates a group
    # it will add new group to all chats database
    # and additionally return that new groups uid
    def add_group(GNAME):
        #create table if not exists
        create_database.create_message_list_database()
        try:
            # imsert new group 
            connection = connect.message_list_database()
            cursor = connection.cursor()
            cursor.execute("""
                            INSERT INTO all_chats (GNAME)
                            VALUES(?)
                            """,(GNAME,))
            cursor.commit()
            
            
            #fetch tbw new group GUID
            cursor.execute("""
                            FROM all_chats SELECT GUID WHERE GNAME= ?
                            """,(GNAME,))
            RESULT = cursor.fetchone()
            return RESULT[0] # retur the GUID (imteger)
        except Exception as e:
            print(e)
            return False
        finally:
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
            connection = connect.user_chats_list_database()
            cursor = connection.cursor()
            cursor.execute(f"""
                                INSERT INTO CHATS_{str(UID)} (GUID,GNAME)
                                VALUES (?,?)
                            """, 
                            (GUID, GNAME,))
            connection.commit()
        except Exception as e:
            print(e)
        finally:
            connection.close()
    
    # it will store messages
    # each group id represents that specific table
    # this table contains all messages 
    def store_this_message(GROUP_ID, SENDER_ID, SENDER_NAME, MESSAGE):
        create_database.create_chat_database_table(GROUP_ID)
        try:
            connection = connect.messages_database()
            cursor = connection.cursor()
            cursor.execute(f"""
                    INSERT INTO G_{GROUP_ID} (SENDER_ID, SENDER_NAME, MESSAGE)
                    VALUES(?, ?, ?)
            """, (int(SENDER_ID), SENDER_NAME, MESSAGE))
            connection.commit()
            MESSAGE_ID = cursor.lastrowid
            cursor.execute(f"""
                            SELECT TIME_STAMP FROM G_{str(GROUP_ID)} WHERE MESSAGE_ID = ?
                            """,(MESSAGE_ID,))
            
            result = cursor.fetchone()
            print(result)
            return MESSAGE_ID, result[0]
        except Exception as e:
            print(e)
            return False, False
        finally:
            if connection:
                connection.close()


