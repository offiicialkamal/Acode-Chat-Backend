from .connect import database

#in future ill add some more metjods like passwod mail number dob changing
class update:
    def otp(new_otp, UID, COOKIE):
        try:
            connection = database.connect_users_db()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                                UPDATE users 
                                SET IS_MAIL_OTP = ?
                                WHERE UID = ? AND COOKIE = ?
                                """,(new_otp, UID, COOKIE))
                connection.commit()
                cursor.close()
                return True
        except Exception as e:
            print(f"err while upgrading otp {e}")
        finally:
            if connection:
                connection.close()
    
    # improve it if iser wants blocking a user or lefting from chat
    def user_groups_list():
        try:
            connection = database_connection.connection()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                                INSERT INTO 
                                """)
        except Exception as e:
            print("error on user_groups_list():", e)
        finally:
            if connection:
                connection.close()