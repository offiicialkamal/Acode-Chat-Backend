from flask import Flask, request
import json
import random

app=Flask("__name__")

def provide_database():
    with open("users_database.json", "r") as f:   
        # DATBASE_JSON  = f.read()
        return json.load(f)

def write_in_database(new_users_data):
    try:
        with open("users_database.json", "w") as f:
            json.dump(new_users_data, f, indent=4)
            return True
    except Exception as e:
        print(f"error while writing new user in database {new_users_data} \n \n \n {e}")
        return False

def update_database(data_to_update):
    with open("users_database.json", "w") as f:
        f.update(data_to_update)
        
    
def provide_new_id():
    new_id = str(random.randint(100000000, 9999999999))
    return new_id


def create_new_account(name, email, number, password, location):
    data = {
        provide_new_id():{
                    "name": name,
                    "email": email,
                    "number": number,
                    "password": password,
                    "location": location,
                    "cookie": generate_cookie_string(),
                    "accessToken": generate_new_accessToken(),
                    "lastLogin": dateTime,
                    "accountCreationDateTime": get_date_time_now()
        }
    }






# print(provide_database())
# print(type(provide_database()))
# print(type(num1 := provide_new_id()))
# print(num1)

@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        request.form.get("email")
        request.form.get("password")