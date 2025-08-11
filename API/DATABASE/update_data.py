from .connect import connect

#in future ill add some more metjods like passwod mail number dob changing
class update:
    def otp(new_otp, UID, COOKIE):
        try:
            connection = connect.all_users_table()
            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                                UPDATE users 
                                SET IS_MAIL_OTP = ?
                                WHERE UID = ? AND COOKIE = ?
                                """,(new_otp, UID, COOKIE))
                connection.commit()
                return True
        except Exception as e:
            print(e)
        finally:
            if connection:
                connection.close()
                