from .connect import connect

class get:
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
        finally:
            connection.close()
            
    def stored_otp(UID, COOKIE):
        try:
            connection = connect.all_users_table()
            cursor = connection.cursor()
            cursor.execute("""
                            SELECT IS_MAIL_OTP FROM users WHERE COOKIE = ? AND UID = ?
                            """, (COOKIE,UID,))
            otp = cursor.fetchone()
            print(otp[0])
            return otp[0]
        except Exception as e:
            print(e)
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
        except Exception as e:
            print(e)
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
        finally:
            connection.close()
    
    def first_name(UID):
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
        finally:
            if connection:
                connection.close()
                
                
    def all_chats_json(UID):
        try:
            connection = connect.user_chats_list_database()
            if connection:
                cursor = connection.cursor()
        except Exception as e:
            print(f'erro while getting the chats of {UID} ==>> {e}')
        finally:
            connection.close()
            
        
    
    