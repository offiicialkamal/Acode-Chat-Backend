from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS
from API.GENERAL.new_id import generate_id
from API.GENERAL.cookie import generate_cookie
from API.GENERAL.token import generate_token
from API.DATABASE.database_actions import database
import sqlite3, random, string

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
    return "API is Alive"

@app.route('/sign_up', methods=["GET","POST"])
def signup():
    if request.method == "POST":
        data = request.get_json()
        return jsonify({"message": "signup sucess plesae login", "COOKIE":"this is a  cookie", "UID":"thisd is an uid", "TOKEN": "this is an token"}),200
    elif request.method == "GET":
        return render_template('sign-up.html')
    else:
        return jsonify({"message":"method not allowed or invaled method"}), 405






        






@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        data = request.get_json()
        print(request)
        print(data)
        
        PROVIDED_EMAIL = data.get('EMAIL')
        PROVIDED_PASS = data.get('PASSWORD')
        
        if PROVIDED_EMAIL and PROVIDED_PASS:
            if PROVIDED_EMAIL == 'user1@gamil.com' and PROVIDED_PASS == '1234':
                print('login sucessfull')
                # return a dummy data for now
                return jsonify({"COOKIE": "COOKIE@cookie.com", "UID": "12527383838"}), 200
            else:
                return jsonify({"message":"Invalid username or password ! "}), 401
        else:
            return jsonify({"message":"Invalid username or password ! "}), 401
            
    elif request.method == 'GET':
        return render_template('login.html'), 200

@app.route("/create_new_account", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        data = {
            "id": generate_id(),
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "number": request.form.get("number", "not provided"),
            "dob": request.form.get("DOB", "not provided"),
            "password": request.form.get("password"),
            "location": request.form.get("ip_info"),
            "cookie": generate_cookie(),
            "accessToken": generate_token(),
            "lastLogin": request.form.get("dateTime"),
            "last_pw_change": request.form.get("dateTime"),
            "accountCreationDateTime": request.form.get("dateTime")
        }
        with db_conn() as conn:
            conn.execute('''
                INSERT INTO users (id, name, email, number, dob, password, location, cookie, accessToken, lastLogin, last_pw_change, accountCreationDateTime)
                VALUES (:id, :name, :email, :number, :dob, :password, :location, :cookie, :accessToken, :lastLogin, :last_pw_change, :accountCreationDateTime)
            ''', data)
        return jsonify({"message": "Account created"}), 201
    return render_template("create_account.html")

@app.route("/reset_password", methods=["POST", "GET"])
def reset_password():
    if request.method == "POST":
        user_id = request.form.get("userID")
        new_password = request.form.get("new_password")
        otp = request.form.get("enterd_otp")
        now = request.form.get("todays_date")

        # For now, mock OTP validation (you should implement proper OTP logic)
        if otp != "123456":
            return jsonify({"message": "Invalid OTP"}), 401

        with db_conn() as conn:
            cur = conn.execute("UPDATE users SET password=?, last_pw_change=? WHERE id=?", (new_password, now, user_id))
            if cur.rowcount:
                return jsonify({"message": "Password updated"}), 200
            else:
                return jsonify({"message": "User not found"}), 404
    return render_template("otp.tml")

# @app.route("/get_messages", methods=["POST"])
# def get_messages():
#     thread_id = request.form.get("thread_id")
#     user_id = request.form.get("user_id")
#     cookie = request.form.get("cookie")

#     with db_conn() as conn:
#         cur = conn.execute("SELECT cookie FROM users WHERE id=?", (user_id,))
#         row = cur.fetchone()
#         if not row or row[0] != cookie:
#             return jsonify({"message": "Invalid user"}), 401

#         messages = conn.execute(
#             "SELECT sender_id, sender_name, message, timestamp FROM messages WHERE thread_id=? ORDER BY timestamp ASC",
#             (thread_id,)
#         ).fetchall()

#         return jsonify([
#             {
#                 "sender_id": msg[0],
#                 "sender_name": msg[1],
#                 "message": msg[2],
#                 "timestamp": msg[3]
#             }
#             for msg in messages
#         ])

# @app.route("/get_groups", methods=["POST"])
# def get_user_groups():
#     user_id = request.form.get("user_id")
#     cookie = request.form.get("cookie")

#     with db_conn() as conn:
#         cur = conn.execute("SELECT cookie FROM users WHERE id=?", (user_id,))
#         row = cur.fetchone()
#         if not row or row[0] != cookie:
#             return jsonify({"message": "Invalid session"}), 401

#         groups = conn.execute(
#             "SELECT group_id FROM user_groups WHERE user_id=?",
#             (user_id,)
#         ).fetchall()

#         return jsonify([g[0] for g in groups])


@app.route("/join_group", methods=["POST"])
def join_group():
    user_id = request.form.get("user_id")
    group_id = request.form.get("group_id")
    cookie = request.form.get("cookie")

    with db_conn() as conn:
        cur = conn.execute("SELECT cookie FROM users WHERE id=?", (user_id,))
        row = cur.fetchone()
        if not row or row[0] != cookie:
            return jsonify({"message": "Invalid user"}), 401

        conn.execute("INSERT INTO user_groups (user_id, group_id) VALUES (?, ?)", (user_id, group_id))
        return jsonify({"message": f"User {user_id} joined group {group_id}"}), 200


@socketio.on("connect_user")
def handle_user_connect(data):
    print(" new  user/clint has been connected ")
#     user_id = data.get("user_id")
#     cookie = data.get("cookie")

#     with db_conn() as conn:
#         cur = conn.execute("SELECT cookie FROM users WHERE id=?", (user_id,))
#         row = cur.fetchone()
#         if not row or row[0] != cookie:
#             emit("error", {"message": "Invalid session"})
#             return

#         groups = conn.execute("SELECT group_id FROM user_groups WHERE user_id=?", (user_id,)).fetchall()
#         for (group_id,) in groups:
#             join_room(group_id)
#         emit("connected", {"joined_rooms": [g[0] for g in groups]})





####################################################################################
####################################################################################
############################# SOCKET IO ROUTES/EVENTS ##############################
####################################################################################
####################################################################################
@socketio.on("get_token")
def return_the_token(data):
    print(f"user is asking for its token ====>>>> {data}")
    if data:
        PROVIDED_UID = data.get("UID")
        PROVIDED_COOKIE = data.get("COOKIE")
        
        ORG_COOKIE = 'COOKIE@cookie.com'
        ORG_ACCESS_TOKEN = 'THISISACCESSTOKEN'
        
        if PROVIDED_UID and PROVIDED_COOKIE:
            if ORG_COOKIE:
                # now user has enterd the currect cookie or not lets compare
                if ORG_COOKIE == PROVIDED_COOKIE:
                    # now Asuming the user has enrterd the currect cookie
                    # so we have to returrn the access token of him for message access
                    print('user authenticated sucessfully and token has been sent')
                    return {"status_code": 200, "message": "successfully gotten token", "ACCESS_TOKEN": ORG_ACCESS_TOKEN, "UID": PROVIDED_UID}
                else:
                    return {"status_code": 401, "message": "invalid cookies provided ! login needed"}
            else:
                return {"status_code": 400, "message": "BAD REQUEST ! usder not found"}
        else:
            return {"status_code": 400, "message": "Acces Denaid UID or COOKIES missing !"}
    else:
        return {"status_code": 400, "message": "data field is missing ecpected a JSON data"}

@socketio.on("get_all_messages")
def wants_all_his_chats(data):
    #clint sends a json object im storing that json object on data variable
    print(f"sended data from clint is =>>>>> {data}")
    UID = data.get('UID')
    ACCESS_TOKEN = data.get("ACCESS_TOKEN")
    
    if not UID or not ACCESS_TOKEN:
        return {"status_code": 401, "message": "accesToken or UID is missing"}
    
    ### compare the data UID and accessTokens are valid or not from database
    if UID in ["12527383838"] and ACCESS_TOKEN == 'THISISACCESSTOKEN':
        print("user authenticated now")
        users_all_chats_in_json = {
            "2537623766": {
                "name": "ITS A GROUP A NAME",
                "admin": "74674"
            },
            "476467746788": {
                "name": "its second group",
                "GUID": "2578875588532214",
                "admin": "3666"
            },
            "253762766": {
                "name": "ITS A GROUP A NAME",
                "admin": "74674"
            },
            "47646746788": {
                "name": "its second group",
                "GUID": "2578875588532214",
                "admin": "3666"
            },
            "253762366": {
                "name": "ITS A GROUP A NAME",
                "admin": "74674"
            },
            "47646774688": {
                "name": "its second group",
                "GUID": "2578875588532214",
                "admin": "3666"
            },
             "2537987623766": {
                "name": "ITS A GROUP A NAME",
                "admin": "74674"
            },
            "476467742456788": {
                "name": "its second group",
                "GUID": "2578875588532214",
                "admin": "3666"
            },
            "25376298766": {
                "name": "ITS A GROUP A NAME",
                "admin": "74674"
            },
            "4764673546788": {
                "name": "its second group",
                "GUID": "2578875588532214",
                "admin": "3666"
            },
            "25376245366": {
                "name": "ITS A GROUP A NAME",
                "admin": "74674"
            },
            "4764677468988": {
                "name": "its second group",
                "GUID": "2578875588532214",
                "admin": "3666"
            },
             "2537623355766": {
                "name": "ITS A GROUP A NAME",
                "admin": "74674"
            },
            "47646774076788": {
                "name": "its second group",
                "GUID": "2578875588532214",
                "admin": "3666"
            },
            "253765782766": {
                "name": "ITS A GROUP A NAME",
                "admin": "74674"
            },
            "47646742326788": {
                "name": "its second group",
                "GUID": "2578875588532214",
                "admin": "3666"
            },
            "25376132366": {
                "name": "ITS A GROUP A NAME",
                "admin": "74674"
            },
            "47646774600988": {
                "name": "its second group",
                "GUID": "2578875588532214",
                "admin": "3666"
            }
        }
        return {"status_code": 200, "chats": users_all_chats_in_json}
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