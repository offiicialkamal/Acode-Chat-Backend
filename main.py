from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, join_room, emit, leave_room
import json
import random

app=Flask("__name__")
socket = SocketIO(app, cors_allowed_origins="*")

def provide_new_id():
    new_id = str(random.randint(100000000, 9999999999))
    old_database = provide_database()
    if new_id not in list(old_database.keys()):
        return new_id
    else:
        print("id is already avilable findng again")
        return provide_new_id()

def provide_database():
    with open("users_database.json", "r") as f:   
        return json.load(f)

def broadcast_message(THREAD_ID, SENDER_ID, SENDER_NAME, MESSAGE):
    # send message through web sockets  to that thread id
    # ill implement it later
    # print|("message sent sucessfully")
    # return True
    socket.emit("new_message", {
            "THREAD_ID": THREAD_ID,
            "SENDER_ID": SENDER_ID,
            "SENDER_NAME": SENDER_NAME,
            "MESSAGE": MESSAGE
        }, room=(str(THREAD_ID))
    )
    return True

class Thred_handler:
    def write_message_to_group_database(THREAD_ID, SENDER_ID, SENDER_NAME, MESSAGE):
        #write the message with the detail
        # ill give a message id to each messsage for easy short 
        # ill also give a time stamp for future usAGE 
        print("created or writen to existing THREAD_ID.json file")
        return True
    
    def write_message_to_group_database(MESSAGE_ID, DELETED_BY_NAME, DELETED_BY_ID)
        print("message was deleted sucessfully")
        return True

class User_data_provider():
    def provide_users_database(userID):
        all_data_base = provide_database()
        if userID in all_data_base:
            return all_data_base.get(userID)
        else:
            return False

    # def provide_users_email(userID):
    #     all_data_base = provide_database()
    #     if userID in all_data_base:
    #         return all_data_base[userID].ge("email")
    #     else:
    #         print(f"{userID} not found in database")
    #         return False
        
    def provide_users_data_field(userID, field_name)
        all_data_base = provide_database()
        if userID in list(all_data_base.keys()):
            if data := all_data_base[userID].get(field_name):
                return data
            else:
                message = f"{userID} has no data field {field_name}"
                print(message)
                return False
        else:
            message = f"{userID} not found in exicting database"
            print(message)
            return False
        
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

@app.route("/", methods=["GET"])
def home():
    return "api is alive"

@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        request.form.get("email")
        request.form.get("password")

@app.route("/create_new_account", methods=["GET", "POST"])
def create_acc():
    if request.method == "POST":
        #its an api call 
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
    elif request.method == "GET":
        return render_template("create_account.html")

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
    
# now ill wrirte A route called /send
# its function recive chat id and and message 
# then web socketr will broad cast that message to that specific thread id
#  with the sender name and it s id 

# @app.route("messages/send", methods=["POST"])

@socketio.on("send_message")
def send_message(data):
    SENDER_ID = data.get('user-id')
    COOKIE = data.get('cookie')
    THREAD_ID = data.get("thread_id") # group id i think ill create a json file for each thread id sence i have no database
    MESSAGE = data.get('message')

    #now find the users database to get its cookie string 
    # so that weell able to verify that the user is logged in or not 
    REAL_COOKIE = User_data_provider.provide_users_data_field(SENDER_ID, "cookie")
    if REAL_COOKIE:
        if COOKIE and  REAL_COOKIE == COOKIE:
            # USER AUTHENTICATED SUCESSFULLY
            # NOW WE HAVE TO BROADCAST THAT MESSAGE TO ALL CONNECTED USERS THROUGH WEB SOCKET
            SENDER_NAME = User_data_provider.provide_users_data_field(SENDER_ID, 'name')
            if broadcast_message(THREAD_ID, SENDER_ID, SENDER_NAME, MESSAGE):
                Thred_handler.write_message_to_group_database(THREAD_ID, SENDER_ID, SENDER_NAME, MESSAGE)
                return jsonify({"message": "message sent sucessfully"}), 200
            else:
                return 500
        else:
            return jsonify({"message": "you need to login again", "redirect_login": True}), 401



#ill handle all request =s in next commit