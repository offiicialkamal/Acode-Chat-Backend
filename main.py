from flask import Flask, request, jsonify, render_template
import json
import random

app=Flask("__name__")
def provide_new_id():
    new_id = str(random.randint(100000000, 9999999999))
    # now check this id is not given to any user before
    # first get the database keys  list and thn check using in keyword
    old_database = provide_database()
    if new_id not in list(old_database.keys()):
        return new_id
    else:
        print("id is already avilable findng again")
        provide_new_id()

def provide_database():
    with open("users_database.json", "r") as f:   
        return json.load(f)

def write_in_database(data_to_update):
    old_database = provide_database()
    with open("users_database.json", "w") as f:
        # old_database[list(data_to_update.keys())[0]] = data_to_update
        old_database[data_to_update.get("id")] = data_to_update
        json.dump(old_database, f, indent=4)        

def update_database(userID, key, value):
    old_database = provide_database()
    with open("users_database.json", "w") as f:
        old_database.get(userID)[key] = value
        json.dump(old_database, f, indent=4)
        

def generate_cookie_string():
    return "fbabasd iasddibasdhbhasdib saasdlbasdib asdciasdib asdiliibbsdliu "

def generate_new_accessToken():
    return "oduauyyasgasygdyasiuasasdliasdi"

def get_date_time_now():
    return "its date time now"

def create_new_account(name, email, number, DOB, password, location, dateTime):
    data = {
        "id": provide_new_id(),
        "name": name,
        "email": email,
        "number": number,
        "DOB": DOB,
        "password": password,
        "location": location,
        "cookie": generate_cookie_string(),
        "accessToken": generate_new_accessToken(),
        "lastLogin": dateTime,
        "last_pw_change": dateTime,
        "accountCreationDateTime": dateTime
        }
    
    write_in_database(data)


@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        request.form.get("email")
        request.form.get("password")

@app.route("/create_new_account", methods=["GET", "POST"])
def create_acc():
    #collect all data and pass on write data function
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    location = request.form.get("ip_info")
    dateTime = request.form.get("dateTime")
    number = request.form.get("number") if request.form.get("number") else "not provided"
    DOB = request.form.get("DOB") if request.form.get("DOB") else "not provided"
    ## now write all a=dat to the program
    create_new_account(name, email, number, DOB, password, location, dateTime)

@app.route("/reset_password", methods=["GET", "POST"])
def reset_pw_home():
    global sended_otp
    # check the otp and reste the password on request
    if request.method == "POST":        #using post method because of its a secure method
        userID = request.form.get("userID")
        new_password = request.form.get("new_password")
        enterd_otp = request.form.get("enterd_otp")
        last_pw_change = request.form.get("todays_date")
        if userID in list(provide_database.keys()) and enterd_otp == sended_otp:
            ## sucessfully user verified
            update_database(
                userID,
                "password",
                new_password
            )
            update_database(
                userID,
                "last_pw_change",
                last_pw_change
            )
        else:
            print("wrong otp provided")
            return jsonify({"message": "wrong otp"}), 401
    elif request.method == "GET":
        return render_template("otp.html")
    else:
        return jsonify({"message": "Method not allowed"}), 401
    


#ill handle all request =s in next commit