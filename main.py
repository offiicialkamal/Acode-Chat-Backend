from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS
# from API.GENERAL.new_id import generate_id
from API.GENERAL.cookie import create_cookie
from API.GENERAL.token import create_token
from API.GENERAL.otp import generate_otp
from API.GENERAL.send_verification_email import sendOTP
#from API.DATABASE.createDatabase import create_database
#from API.DATABASE.database_actions import database
from API.DATABASE.write_data import write_in_database
from API.DATABASE.get_data import get
from API.DATABASE.update_data import update
import sqlite3, random, string, time

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


############################################################################
############################################################################
######################## PLACEHOLDER DATABASES #############################
############################################################################
############################################################################
originalDatabase = {
        "accessToken": "tyadittfiugweoyggqewoyggewoyg"
    }
originalMessageDatabase = {
        "group id 1":{
            "message id 1":{
                "sender uid": "734736473",
                "message": "hello brother"
            },
            "message id 2":{
                "sender uid ": "56354635",
                "message": "hello from user 2"
            }
        },
        "group id 2":{
            "message id 1":{
                "sender uid": "734736473",
                "message": "hello brother"
            },
            "message id 2":{
                "sender uid ": "56354635",
                "message": "hello from user 2"
            }
        },
        "group id 3":{
            "message id 1":{
                "sender uid": "734736473",
                "message": "hello brother"
            },
            "message id 2":{
                "sender uid ": "56354635",
                "message": "hello from user 2"
            }
        }
    }

usersDatbase = {
    "1111":{
        "name": "kamal",
        "email": "example1@gmail.com",
        "cookie": "hdhsuedususus",
        "accessToken": "sujefbbddujssjsn"
    },
    "2222":{
        "name": "kamal",
        "email": "example1@gmail.com",
        "cookie": "hdhsuedususus",
        "accessToken": "sujefbbddujssjsn"
    },
    "3333":{
        "name": "kamal",
        "email": "example1@gmail.com",
        "cookie": "hdhsuedususus",
        "accessToken": "sujefbbddujssjsn"
    }
}













def db_conn(databaseNAME):
    if databaseNAME == "messages":
        return sqlite3.connect("messages.db")
    elif databaseNAME == "users":
        return sqlite3.connect("usersDatabase.db")
    else:
        return 
    

@app.route("/")
def home():
    print(request.remote_addr)
    return "API is Alive"

@app.route('/sign_up', methods=["GET","POST"])
def signup():
    DEFAULT_CHAT_UID = None
    DEFAULT_CHAT_NAME = None
    NEW_USERS_UID = None
    EMAIL= None
    data = None
    FIRST_NAME = None
    LAST_NAME = None
    PHONE_NO = None
    all_emails = None
    IS_MAIL_OTP = None
    PASSWORD = None
    TOKEN = None
    COOKIE = None
    CITY = None
    IP = None
    if request.method == "POST":
        DEFAULT_CHAT_UID = "1000000000000"
        DEFAULT_CHAT_NAME = "ACODE CHAT"
        print(request.remote_addr)
        data = request.get_json()
        print(data)
        EMAIL = data.get('EMAIL')
        all_emails = get.all_emails()
        print(all_emails)
        if not all_emails or (f'{EMAIL}',) not in all_emails:
            FIRST_NAME = data.get('FIRST_NAME')
            LAST_NAME = data.get('LAST_NAME')
            DOB = data.get('DOB')
            PHONE_NO = int(data.get('PHONE_NO'))
            PASSWORD = data.get('PASSWORD')
            IP = data['IP_INFO'].get('ip')
            CITY = data['IP_INFO'].get('city')
            IS_MAIL_OTP = generate_otp()
            TOKEN = create_token()
            COOKIE = create_cookie()
            # write all data in database
            NEW_USERS_UID = write_in_database.add_user(FIRST_NAME, LAST_NAME, EMAIL, IS_MAIL_OTP, DOB, PHONE_NO, IP, CITY,PASSWORD, TOKEN, COOKIE)
            ## add to defaul chat group
            write_in_database.add_user_in_group(NEW_USERS_UID, DEFAULT_CHAT_UID, DEFAULT_CHAT_NAME)
            # retun sucess message along with cookie token and uid
            # ill add verification machenism
            
            sendOTP(EMAIL,IS_MAIL_OTP, FIRST_NAME,"otpForNewAcc")
            return jsonify({"message": "Details Got sucessfully, verification pendding !", "COOKIE":COOKIE, "UID":NEW_USERS_UID, "TOKEN":TOKEN}),200
        else:
            return jsonify({"message": "Email already Associated with another Account"}), 409
    elif request.method == "GET":
        return render_template('sign-up.html')
    else:
        return jsonify({"message":"method not allowed or invaled method"}), 405

@app.route('/account_verification',methods=["POST"])
def verify_otp():
    data = request.get_json()
    enterd_otp = data.get('ENTERD_OTP')
    UID = data.get("UID")
    COOKIE = data.get("COOKIE")
    if UID and COOKIE:
        if enterd_otp == str(get.stored_otp(UID, COOKIE)):
            update.otp(0, UID, COOKIE)
            return jsonify({"message":"Email verified sucessfully", "TOKEN": get.token(COOKIE)}),200
        else:
            return jsonify({"message": "Access Denaid ! Invalid otp"}), 401
    else:
        return jsonify({"message": "missing cookie or uid"})

# if ussr logs in with mail password
@app.route("/login", methods=["GET", "POST"])
def login():
    PROVIDED_EMAIL = None
    PROVIDED_PASS = None
    STORED_PASSWORD = None
    all_emails = None
    data = None
    COOKIE = None
    UID = None
    otp = None
    if request.method == 'POST':
        data = request.get_json()
        # print(data)
        # print(type(data))
        PROVIDED_EMAIL = data.get('EMAIL')
        PROVIDED_PASS = data.get('PASSWORD')
        # print(type(PROVIDED_EMAIL))
        if PROVIDED_EMAIL and PROVIDED_PASS:
            all_emails = get.all_emails()
            if (f'{PROVIDED_EMAIL}',) in all_emails:
                STORED_PASSWORD = get.password(PROVIDED_EMAIL)
                if PROVIDED_PASS == STORED_PASSWORD:
                    COOKIE = get.cookie(PROVIDED_EMAIL)
                    UID = get.uid_by_email(PROVIDED_EMAIL)
                    otp = get.stored_otp(UID, COOKIE)
                    
                    print(f"OTP GOT {otp}")
                    if len(f"{otp}") == '0':
                        return jsonify({"message": "logged in sucessfully", "COOKIE": COOKIE, "UID": UID, "TOKEN": get.token(COOKIE)}),200
                    else:
                       # sendOTP(PROVIDED_EMAIL, otp, get.first_name(UID),"otpForNewAcc")
                        return jsonify({"message": "Access Denaid ! Verification pending", "redirect": True}),401
                else:
                    return jsonify({"message": "invalid password"}),401
            else:
                return jsonify({"message": "No account associated with provided account"}), 401
        else:
            return jsonify({"message":"Access Denaid ! Email or password missing"}), 401
    elif request.method == 'GET':
        return render_template('login.html'), 200
    else:
        return jsonify({"message": "Access Denaid ! invalid method"}), 405

## if user logs in with cookie
@app.route('/get_token', methods=["POST"])
def return_token():
    if request.method == 'POST':
        data = request.get_json()
        PROVIDED_COOKIE = data.get('COOKIE')
        PROVIDED_UID = data.get('UID')
        print(data)
        if PROVIDED_COOKIE and PROVIDED_UID:
            ORIGINAL_UID = get.uid_by_cookie(PROVIDED_COOKIE)
            if ORIGINAL_UID and ORIGINAL_UID == PROVIDED_UID:
                stored_otp = get.stored_otp(ORIGINAL_UID, PROVIDED_COOKIE)
               
               
               
                print(len(str(stored_otp)))
                # print(str(stored_otp))
                if len(str(stored_otp)) == 1:
                    return jsonify({"message":"Login sucess", "TOKEN": get.token(PROVIDED_COOKIE)}), 200
                else:
                    #sendOTP(get.email(PROVIDED_COOKIE),str(stored_otp), get.first_name(ORIGINAL_UID),"otpForNewAcc")
                    return jsonify({"message": "Verification pending"}), 409
            else:
                return jsonify({"message": "Access Denaid ! Login needed"}), 400
        else:
            return jsonify({"mesaage":"Access Denaid ! missing cookie or uid"})
    else:
        return jsonify({"message": "Access Denaid ! imvalid method"}), 405

# @app.route("/reset_password", methods=["POST", "GET"])
# def reset_password():
#     if request.method == "POST":
#         user_id = request.form.get("userID")
#         new_password = request.form.get("new_password")
#         otp = request.form.get("enterd_otp")
#         now = request.form.get("todays_date")

#         # For now, mock OTP validation (you should implement proper OTP logic)
#         if otp != "123456":
#             return jsonify({"message": "Invalid OTP"}), 401

#         with db_conn() as conn:
#             cur = conn.execute("UPDATE users SET password=?, last_pw_change=? WHERE id=?", (new_password, now, user_id))
#             if cur.rowcount:
#                 return jsonify({"message": "Password updated"}), 200
#             else:
#                 return jsonify({"message": "User not found"}), 404
#     return render_template("otp.tml")

# @app.route("/join_group", methods=["POST"])
# def join_group():
#     user_id = request.form.get("user_id")
#     group_id = request.form.get("group_id")
#     cookie = request.form.get("cookie")

#     with db_conn() as conn:
#         cur = conn.execute("SELECT cookie FROM users WHERE id=?", (user_id,))
#         row = cur.fetchone()
#         if not row or row[0] != cookie:
#             return jsonify({"message": "Invalid user"}), 401

#         conn.execute("INSERT INTO user_groups (user_id, group_id) VALUES (?, ?)", (user_id, group_id))
#         return jsonify({"message": f"User {user_id} joined group {group_id}"}), 200


@socketio.on("connect_user")
def handle_user_connect(data):
    print(" new  user/clint has been connected ")
    
####################################################################################
####################################################################################
############################# SOCKET IO ROUTES/EVENTS ##############################
####################################################################################
####################################################################################
# @socketio.on("get_token")
# def return_the_token(data):
#     print(f"user is asking for its token ====>>>> {data}")
#     if data:
#         PROVIDED_UID = data.get("UID")
#         PROVIDED_COOKIE = data.get("COOKIE")
        
#         ORG_COOKIE = 'COOKIE@cookie.com'
#         ORG_ACCESS_TOKEN = get.token(PROVIDED_UID)
        
#         if PROVIDED_UID and PROVIDED_COOKIE:
#             if ORG_COOKIE:
#                 # now user has enterd the currect cookie or not lets compare
#                 if ORG_COOKIE == PROVIDED_COOKIE:
#                     # now Asuming the user has enrterd the currect cookie
#                     # so we have to returrn the access token of him for message access
#                     print('user authenticated sucessfully and token has been sent')
#                     return {"status_code": 200, "message": "successfully gotten token", "ACCESS_TOKEN": ORG_ACCESS_TOKEN, "UID": PROVIDED_UID}
#                 else:
#                     return {"status_code": 401, "message": "invalid cookies provided ! login needed"}
#             else:
#                 return {"status_code": 400, "message": "BAD REQUEST ! usder not found"}
#         else:
#             return {"status_code": 400, "message": "Acces Denaid UID or COOKIES missing !"}
#     else:
#         return {"status_code": 400, "message": "data field is missing ecpected a JSON data"}

@socketio.on("get_all_chat_list")
def wants_all_his_chats(data):
    #clint sends a json object im storing that json object on data variable
    print(f"sended data from clint is =>>>>> {data}")
    PROVIDED_UID = data.get('UID')
    ACCESS_TOKEN = data.get("TOKEN")
    
    if not PROVIDED_UID or not ACCESS_TOKEN:
        return {"status_code": 401, "message": "accesToken or UID is missing"}
    
    ### compare the data UID and accessTokens are valid or not from database
    UID = get.uid_by_token(ACCESS_TOKEN)
    if UID == PROVIDED_UID:
        all_chats_json = get.all_chats_json(UID)
        print(all_chats_json)
        print(type(all_chats_json))
        if all_chats_json:
            return {"message":"Sucessfully Got Chats", "status_code":200, "chats":all_chats_json}
        else:
            return {"mesaage":"Internal Server Err !", "status_code": 500}
    else:
        print('Access Denaid !')
        return {"status_code": 401, "message": "Access Denaid ! invalid token you need to login again"}

@socketio.on('open_a_chat')
def wants_to_open_the_chat(data):
    # now we have to return the all messages of that specific chat and clint should use cllbacks to recieve data, all is in json formate
    if data:
        if data.get("accessToken") == originalDatabase.get('accessToken'):
            print("currect access token")
            all_messages = originalMessageDatabase.get("groupUID")
            return {"status_code": 200, "message": "sucess", "messages": all_messages}
        else:
            print("acceess denaid")
            return {"status_code": 401, "message": "Access Denaid !"}
    else:
        return {"status_code": 401, "message": "Access Denaid !"}

@socketio.on("send_message")
def handle_send_message(data):
    sender_id = data.get("user-id")
    cookie = data.get("cookie")
    thread_id = data.get("thread_id")
    message = data.get("message")
    with db_conn() as conn:
        cur = conn.execute("SELECT name, cookie FROM users WHERE id=?", (sender_id,))
        row = cur.fetchone()
        if not row:
            emit("error", {"message": "User not found"}, room=request.sid)
            return
        name, real_cookie = row
        if real_cookie != cookie:
            emit("error", {"message": "Invalid session"}, room=request.sid)
            return

        conn.execute("INSERT INTO messages (thread_id, sender_id, sender_name, message) VALUES (?, ?, ?, ?)",
                     (thread_id, sender_id, name, message))
        socketio.emit("new_message", {
            "THREAD_ID": thread_id,
            "SENDER_ID": sender_id,
            "SENDER_NAME": name,
            "MESSAGE": message
        }, room=thread_id)

if __name__ == "__main__":
    socketio.run(app, port=5000, host="0.0.0.0", allow_unsafe_werkzeug=True, debug=True)