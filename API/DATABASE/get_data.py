from .connect import connect
from .createDatabase import create_database
import sys
import json
class get:
    create_database.create_users_database()
    def all_emails():
        try:
            connection = connect.all_users_table()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                                    SELECT EMAIL FROM users
                                """)
                return cursor.fetchall()
        except Exception as e:
            print(e)
            return False
        finally:
            connection.close()
    
    def all_users():
        try:
            connection = connect.all_users_table()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                                SELECT FIRST_NAME, LAST_NAME, UID FROM users
                                """)
            all_users_arr = cursor.fetchall()
            return all_users_arr
        except Exception as e:
            print(f'error while fetching all users {e}')
            return False
        finally:
            if connection:
                connection.close()
            
            
    def stored_otp(RAW_UID, COOKIE):
        UID = int(RAW_UID)
        try:
            connection = connect.all_users_table()
            cursor = connection.cursor()
            cursor.execute("""
                            SELECT IS_MAIL_OTP FROM users WHERE COOKIE = ? AND UID = ?
                            """, (COOKIE,UID,))
            otp = cursor.fetchone()
            # print(otp[0])
            return otp[0]
        except Exception as e:
            print(f"unable to get stored otp {e}")
            return False
        finally:
            connection.close()
    
    def password(EMAIL):
        try:
            connection = connect.all_users_table()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                                SELECT PASSWORD FROM users WHERE EMAIL=?
                                """,(EMAIL,))
                password = cursor.fetchone()
                type(password)
                print(password)
                return password[0]
        except Exception as e:
            print(f'Error getting password {e}')
            return False
        finally:
            connection.close()
    
    def email(COOKIE):
        try:
            connection = connect.all_users_table()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                                SELECT EMAIL FROM users WHERE COOKIE=?
                                """,(COOKIE,))
                email = cursor.fetchone()
                return email[0]
        except Exception as e:
            print(e)
            return False
        finally:
            if connection:
                connection.close()
    
    def cookie(EMAIL):
        try:
            connection = connect.all_users_table()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                                SELECT COOKIE FROM users WHERE EMAIL=?
                                """,(EMAIL,))
                cookie = cursor.fetchone()
                return cookie[0]
        except Exception as e:
            print(e)
            return False
        finally:
            connection.close()
    
    def uid_by_email(EMAIL):
        try:
            connection = connect.all_users_table()
            if connection:
                cursor = connection.cursor()
                
                cursor.execute("""
                                SELECT UID FROM users WHERE EMAIL=?
                                """, (EMAIL,))
                
                uid = cursor.fetchone()
                return uid[0]
        except Exception as e:
            print(e)
            return False
        finally:
            connection.close()
    
    def uid_by_cookie(COOKIE):
        try:
            connection = connect.all_users_table()
            if connection:
                cursor = connection.cursor()
                
                cursor.execute("""
                                SELECT UID FROM users WHERE COOKIE=?
                                """, (COOKIE,))
                
                uid = cursor.fetchone()
                return uid[0]
        except Exception as e:
            print(e)
            return False
        finally:
            connection.close()
    
    def uid_by_token(TOKEN):
        try:
            connection = connect.all_users_table()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                                SELECT UID FROM users WHERE TOKEN = ?
                                """,(TOKEN,))
                uid = cursor.fetchone()
                return(uid[0])
            else:
                return False
        except Exception as err:
            print(err)
            return False
        finally:
            if connection:
                connection.close()
            
            
            
    def token(COOKIE):
        try:
            connection = connect.all_users_table()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                                SELECT TOKEN FROM users WHERE COOKIE=?
                                """,(COOKIE,))
                token = cursor.fetchone()
                return token[0]
        except Exception as e:
            print(e)
            return False
        finally:
            connection.close()
    
    def first_name(RAW_UID):
        UID = int(RAW_UID)
        try:
            connection = connect.all_users_table()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                                SELECT FIRST_NAME 
                                FROM users 
                                WHERE UID = ?
                                """,(UID,))
                first_name = cursor.fetchone()
                return first_name[0]
        except Exception as e:
            print(e)
            return False
        finally:
            if connection:
                connection.close()
                
    def last_name(RAW_UID):
        UID = int(RAW_UID)
        try:
            connection = connect.all_users_table()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                                SELECT LAST_NAME FROM users WHERE UID = ?
                                """,(UID,))
                return cursor.fetchone()[0]
        except Exception as e:
            print(e)
        finally:
            connection.close()
                
    def all_chats_json(RAW_UID):
        UID = int(RAW_UID)
        try:
            connection = connect.user_chats_list_database()
            if connection:
                cursor = connection.cursor()
                cursor.execute(f"""
                                SELECT * FROM {'CHATS_'+str(UID)}
                                """)
                chats_json = ""
                chats = cursor.fetchall()
                # print(chats)
                chats_json = {}
                for chat in chats:
                    chats_json[str(chat[0])] = {
                        "NAME": chat[1],
                        "CREATION_DATE": chat[2]
                    }
                return chats_json
        except Exception as e:
            print(f'erro while getting the chats of {UID} ==>> {e}')
            return False
        finally:
            connection.close()
    
    def all_messages_json(limit, guid):
        try:
            connection = connect.messages_database()
            if connection:
                cursor = connection.cursor()
                cursor.execute(f"""
                                SELECT * FROM (
                                 SELECT * FROM G_{str(guid)} 
                                 ORDER BY MESSAGE_ID DESC
                                 LIMIT {limit}
                                 ) sub 
                                 ORDER BY MESSAGE_ID ASC
                                """)
                messages_of_this_group_in_json_dict = {}
                rows_list_type = cursor.fetchall()
                print(rows_list_type)
                for row_tupple in rows_list_type:
                    messages_of_this_group_in_json_dict[str(row_tupple[0])] = {
                            "sender_id": row_tupple[1],
                            "sender_name": row_tupple[2],
                            "message":row_tupple[3],
                            "time_stamp": row_tupple[4]
                        }
                return messages_of_this_group_in_json_dict
        except Exception as e:
            print(e)
            return False
        finally:
            connection.close()
