import sqlite3
def all_personal_data(UID):
        connection = None
        try:
            connection = sqlite3.connect('DB/all_users.db')
            if connection:
                 cursor = connection.cursor()
                 cursor.execute("""
                                SELECT * FROM users WHERE UID=?
                 """,(UID,))
                 raw_data = cursor.fetchall()[0]
                 print(raw_data, type(raw_data))
                 data = {
                     'first_name': raw_data[1],
                     'last_name': raw_data[2],
                     'email': raw_data[3],
                     'dob': raw_data[5],
                     'phone': raw_data[6]
                 }
                 cursor.close()
                 return data
        except Exception as e:
            print(e)
            return None
        finally:
            if connection:
                connection.close()
            
print(all_personal_data('01'))
