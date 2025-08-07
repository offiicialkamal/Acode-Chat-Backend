from .connect import connect

class werite_in_database:
    def add_user(FIRST_NAME, LAST_NAME, EMAIL, DOB, PHONE_NO, IP, CITY,PASSWORD, TOKEN, COOKIE):
        try:
            cursor = connect.all_users_table.cursor()
            if cursor:
                cursor.execute("""
                                INSERT INTO users (FIRST_NAME, LAST_NAME, EMAIL, DOB, PHONE_NO, IP, CITY, PASSWORD, TOKEN, COOKIE)
                                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                """, 
                            (FIRST_NAME, LAST_NAME, EMAIL, DOB, PHONE_NO, IP, CITY,PASSWORD, TOKEN, COOKIE)
                    )
                cursor.commit()
            else:
                return False
        except Exception as e:
            print(e)
        finally:
            cursor.close()
    
    def add_group(UID, GNAME):
        try:
            cursor = connect.user_chats_list_database.cursor()
            cursor.execute("""
                                INSERT INTO CHATS_{UID} (GNAME)
                                VALUES (?)
                            """, 
                            UID, GNAME)
            cursor.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            
    def add_new_messaage(GROUP_ID,GRPUP,SENDER_ID)


