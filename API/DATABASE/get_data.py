from .connect import database
from .createDatabase import create_database
from datetime import datetime
import sys
import json
class get:
    create_database.create_users_database()
    def all_emails():
        try:
            connection = database.connect_users_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                                    SELECT EMAIL FROM users
                                """)
                return cursor.fetchall()
        except Exception as e:
            print("error on all_emails():",e)
            return False
        finally:
            if connection:
                connection.close()
    
    def all_users():
        try:
            connection = database.connect_users_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                                SELECT FIRST_NAME, LAST_NAME, UID FROM users
                                """)
            all_users_arr = cursor.fetchall()
            print(all_users_arr, type(all_users_arr))
            cursor.close()
            return all_users_arr
        except Exception as e:
            print(f"error while fetching all users {e}")
            return False
        finally:
            if connection:
                connection.close()
            
            
    def stored_otp(RAW_UID, COOKIE):
        UID = int(RAW_UID)
        try:
            connection = database.connect_users_db()
            cursor = connection.cursor()
            cursor.execute("""
                            SELECT IS_MAIL_OTP FROM users WHERE COOKIE = ? AND UID = ?
                            """, (COOKIE,UID,))
            otp = cursor.fetchone()
            cursor.close()
            # print(otp[0])
            return otp[0]
        except Exception as e:
            print(f"unable to get stored otp {e}")
            return False
        finally:
            if connection:
                connection.close()
    
    def password(EMAIL):
        try:
            connection = database.connect_users_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                                SELECT PASSWORD FROM users WHERE EMAIL=?
                                """,(EMAIL,))
                password = cursor.fetchone()
                cursor.close()
                return password[0]
        except Exception as e:
            print(f"Error on password(EMAIL): {e}")
            return False
        finally:
            if connection:
                connection.close()
    
    def email(COOKIE):
        try:
            connection = database.connect_users_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                                SELECT EMAIL FROM users WHERE COOKIE=?
                                """,(COOKIE,))
                email = cursor.fetchone()
                cursor.close()
                return email[0]
        except Exception as e:
            print(" eeror on email(COOKIE):",e)
            return False
        finally:
            if connection:
                connection.close()
    
    def cookie(EMAIL):
        try:
            connection = database.connect_users_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                                SELECT COOKIE FROM users WHERE EMAIL=?
                                """,(EMAIL,))
                cookie = cursor.fetchone()
                cursor.close()
                return cookie[0]
        except Exception as e:
            print(" error on cookie(EMAIL):",e)
            return False
        finally:
            if connection:
                connection.close()
    
    def uid_by_email(EMAIL):
        try:
            connection = database.connect_users_db()
            if connection:
                cursor = connection.cursor()
                
                cursor.execute("""
                                SELECT UID FROM users WHERE EMAIL=?
                                """, (EMAIL,))
                
                uid = cursor.fetchone()
                cursor.close()
                return uid[0]
        except Exception as e:
            print(" err on uid_by_email(EMAIL):", e)
            return False
        finally:
            if connection:
                connection.close()
    
    def uid_by_cookie(COOKIE):
        try:
            connection = database.connect_users_db()
            if connection:
                cursor = connection.cursor()
                
                cursor.execute("""
                                SELECT UID FROM users WHERE COOKIE=?
                                """, (COOKIE,))
                
                uid = cursor.fetchone()
                cursor.close()
                return uid[0]
        except Exception as e:
            print("err on uid_by_cookie(COOKIE):", e)
            return False
        finally:
            if connection:
                connection.close()
    
    def uid_by_token(TOKEN):
        try:
            connection = database.connect_users_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                                SELECT UID FROM users WHERE TOKEN = ?
                                """,(TOKEN,))
                uid = cursor.fetchone()
                cursor.close()
                return(uid[0])
            else:
                return False
        except Exception as err:
            print(" err on uid_by_token()",err)
            return False
        finally:
            if connection:
                connection.close()
            
            
            
    def token(COOKIE):
        try:
            connection = database.connect_users_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                                SELECT TOKEN FROM users WHERE COOKIE=?
                                """,(COOKIE,))
                token = cursor.fetchone()
                cursor.close()
                return token[0]
        except Exception as e:
            print("err on token(COOKIE):",e)
            return False
        finally:
            if connection:
                connection.close()
    
    def first_name(RAW_UID):
        UID = int(RAW_UID)
        try:
            connection = database.connect_users_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                                SELECT FIRST_NAME 
                                FROM users 
                                WHERE UID = ?
                                """,(UID,))
                first_name = cursor.fetchone()
                cursor.close()
                return first_name[0]
        except Exception as e:
            print(" err on first_name(RAW_UID):", e)
            return False
        finally:
            if connection:
                connection.close()
                
    def last_name(RAW_UID):
        UID = int(RAW_UID)
        try:
            connection = database.connect_users_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                                SELECT LAST_NAME FROM users WHERE UID = ?
                                """,(UID,))
                return cursor.fetchone()[0]
        except Exception as e:
            print("err on last_name() ", e)
        finally:
            if connection:
                connection.close()
                
    def all_chats_json(RAW_UID):
        UID = int(RAW_UID)
        try:
            connection = database.connect_chat_lists_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute(f"""
                                SELECT * FROM {"CHATS_"+str(UID)}
                                """)
                chats_json = ""
                chats = cursor.fetchall()
                # print(chats)
                chats_json = {}
                for chat in chats:
                    chats_json[str(chat[0])] = {
                        "NAME": chat[1],
                        "PROFILE_PIC": chat[2] if chat[2] else '',
                        "CREATION_DATE": chat[3]
                    }
                cursor.close()
                return chats_json
        except Exception as e:
            print(f"erro while getting the chats of {UID} ==>> {e}")
            return False
        finally:
            if connection:
                connection.close()
    
    def all_messages_json(limit, guid):
        try:
            connection = database.connect_messages()
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
                            "SENDER_ID": row_tupple[1],
                            "SENDER_NAME": row_tupple[2],
                            "MESSAGE":row_tupple[3],
                            "PROFILE_PIC": row_tupple[4],
                            "TIME_STAMP": row_tupple[5]
                        }
                cursor.close()
                return messages_of_this_group_in_json_dict
        except Exception as e:
            print("err on all_messages_json",e)
            return False
        finally:
            if connection:
                connection.close()
    
    def all_personal_data(UID):
        try:
            connection = database.connect_users_db()
            if connection:
                 cursor = connection.cursor()
                 cursor.execute("""
                                SELECT * FROM users WHERE UID=?
                 """,(UID,))
                 
                 fc = cursor.fetchall()
                 print('its fc data', fc)
                 raw_data = fc[0]
                 print('its raw data',raw_data)
                 data = {
                     'FIRST_NAME': raw_data[1],
                     'LAST_NAME': raw_data[2],
                     'EMAIL': raw_data[3],
                     'DOB': raw_data[4],
                     'PHONE': raw_data[5],
                     'PROFILE_PIC': raw_data[7],
                     'COOKIE': raw_data[-4],
                 }
                 cursor.close()
                 return data
        except Exception as e:
            print(e)
            return None
        finally:
            if connection:
                connection.close()
            
