from .connect import database_connection

#in future ill add some more metjods like passwod mail number dob changing
class update:
    def otp(new_otp, UID, COOKIE):
        try:
            connection = database_connection.getconn()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                                UPDATE users 
                                SET IS_MAIL_OTP = %s
                                WHERE UID = %s AND COOKIE = %s
                                """,(new_otp, UID, COOKIE))
                connection.commit()
                cursor.close()
                return True
        except Exception as e:
            print(f"err while upgrading otp {e}")
        finally:
            if connection:
                database_connection.putconn(connection)
    
    # improve it if iser wants blocking a user or lefting from chat
    def user_groups_list():
        try:
            connection = database_connection.getconn()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                                INSERT INTO 
                                """)
        except Exception as e:
            print("error on user_groups_list():", e)
        finally:
            database_connection.putconn(connection)