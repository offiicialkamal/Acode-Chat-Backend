from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from API.GENERAL.cookie import create_cookie
from API.GENERAL.token import create_token
from API.GENERAL.otp import generate_otp
from API.GENERAL.data_validators import validator
from API.GENERAL.send_verification_email import sendOTP
from API.DATABASE.write_data import write_in_database
from API.DATABASE.get_data import get
from API.DATABASE.update_data import update
from GLOBAL_DATABASE_API.data_pusher import clone_replace_push_data
# import requests
import sqlite3
import random
import string
import time
import os
import json
import uvicorn

app = FastAPI()

# Allow all origins (development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your Cordova app origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# application logs show or not
is_developement = True



connected_clients = set()
 #all comnected ckients
rooms = dict() # store all rooms
email_change_otps_dict = dict() # hear ill store the otps for email changing requests 
#esxample strructure
# {
#     "room_id1":{
#             "live_memeber1_id": "socket id",
#             "live_memeber2_id": "socket id"
#         },
#     "room_id2":{
#             "live_memeber1_id": "socket id",
#             "live_memeber2_id": "socket id"
#         }
# }
############№####      OR

# {
#     "room1":["socket1", "socket2", "socket3"],
#     "room2":["socket1", "socket2"]
# }

############################################################################
############################################################################
######################## PLACEHOLDER DATABASES #############################
############################################################################
############################################################################
# originalDatabase = {
  
#                 "sender uid ": "56354635",
#                 "message": "hello from user 2"
#             }
#         },
#         "group id 2":{
#             "message id 1":{
#                 "sender uid": "734736473",
#                 "message": "hello brother"
#             },
#             "message id 2":{
#                 "sender uid ": "56354635",
#                 "message": "hello from user 2"
#             }
#         },
#         "group id 3":{
#             "message id 1":{
#                 "sender uid": "734736473",
#                 "message": "hello brother"
#             },
#             "message id 2":{
#                 "sender uid ": "56354635",
#                 "message": "hello from user 2"
#             }
#         }
#     }

# usersDatbase = {
#     "1111":{
#         "name": "kamal",
#         "email": "example1@gmail.com",
#         "cookie": "hdhsuedususus",
#         "accessToken": "sujefbbddujssjsn"
#     },
#     "2222":{
#         "name": "kamal",
#         "email": "example1@gmail.com",
#         "cookie": "hdhsuedususus",
#         "accessToken": "sujefbbddujssjsn"
#     },
#     "3333":{
#         "name": "kamal",
#         "email": "example1@gmail.com",
#         "cookie": "hdhsuedususus",
#         "accessToken": "sujefbbddujssjsn"
#     }
# }







class socket:
    def emit(self, event, raw_json_data, ws,/,*,room=None):
        ## handle the event
        data = json.dumps(raw_json_data)
        if room & data.get('id') == ws:
            ws.send({
                "event": event,
                "data": data
            })
        # else:
        #     ws.send({
        #         "event":event,
        #         "data":data
        #     })
        
    
    def join_room(self, room_id: str, user_id: str, socket_id: str):
        global rooms
        rooms.setdefault(str(room_id), {})[str(user_id)] = str(socket_id)
        return True
    
            
        

@app.get("/")
def home(request: Request):
    print(request)
    for e in request:
        print(e)
    # requests.get("https://parental-kelci-nothinghjn-df173882.koyeb.app/quick_quick_save_data_to_database_repository")
    # clone_replace_push_data(commit_databases=False)
    return "API is Alive"
  
@app.get("/uptime")
def uptime():
    return "im alive boss"

@app.get("/quick_quick_save_data_to_database_repository")
def data_saver_main():
    clone_replace_push_data()
    return "done cloned and pushed successfully"

@app.get('/sign_up')
def signup_get():
    return render_template("sign-up.html")

    
@app.post("/sign_up")
async def signup(request: Request):
    print(request)
    otp_response = None
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
    PROFILE_PIC = "https://raw.githubusercontent.com/hackesofice/Z/refs/heads/main/Acode-Chat-Plugin/Backend/DEFAULT_PROFILE_PIC.jpeg"
    if PROFILE_PIC:
        data = await request.json()
        DEFAULT_CHAT_UID = "1000000000000"
        DEFAULT_CHAT_NAME = "ACODE CHAT"
        EMAIL = data.get("EMAIL")
        all_emails = get.all_emails()
        write_in_database.add_group(DEFAULT_CHAT_NAME, DEFAULT_CHAT_UID) ## one or only for the first time when we have a new database pr blank database 
        print(all_emails)
        print(request.remote_addr)
        print(data)
        
        if not all_emails or (f"{EMAIL}",) not in all_emails:
            FIRST_NAME = data.get("FIRST_NAME")
            LAST_NAME = data.get("LAST_NAME")
            DOB = data.get("DOB")
            if data.get("PHONE_NO").isdigit():
                PHONE_NO = int(data.get("PHONE_NO"))
            else:
                return jsonify({"message": "Invalid PHONE_NO providede"})
            PASSWORD = data.get("PASSWORD")
            IP = data["IP_INFO"].get("ip")
            CITY = data["IP_INFO"].get("city")
            IS_MAIL_OTP = generate_otp()
            TOKEN = create_token()
            COOKIE = create_cookie()
            if not (FIRST_NAME or LAST_NAME or DOB):
                return {"message": "missing Details"},400
            for ch in FIRST_NAME + LAST_NAME:
                if not ((ch<="z" and ch>="a") or (ch<="Z" and ch>="A")):
                    return {"message": "Only alphabets allowed in names"},400
            
            # retun sucess message along with cookie token and uid
            # ill add verification machenism
            otp_response = sendOTP(EMAIL,IS_MAIL_OTP, FIRST_NAME,"otpForNewAcc")
            print(otp_response)
            if otp_response.get("status_code") == 200:
                NEW_USERS_UID = write_in_database.add_user(FIRST_NAME, LAST_NAME, EMAIL, IS_MAIL_OTP, DOB, PHONE_NO, IP, CITY,PASSWORD, TOKEN, COOKIE, PROFILE_PIC)
                write_in_database.add_user_in_group(NEW_USERS_UID, DEFAULT_CHAT_UID, DEFAULT_CHAT_NAME)
                return {"message": "Details Got sucessfully, verification pendding !", "COOKIE":COOKIE, "UID":NEW_USERS_UID, "TOKEN":TOKEN},200
            elif otp_response.get("status_code") == 429:
                return {"message": "Faild ! Too much requets wait amd retry after 20 minitus"},429
            elif otp_response.get("status_code") == 400:
                return {"message":"Plase check Email"},400
            else:
                return {"message": "faild to send otp", "otp_status": otp_response}, otp_response.get("status_code")
        else:
            return {"message": "Email already Associated with another Account"}, 409
    # elif request.method == "GET":
        
    # else:
    #     return jsonify({"message":"method not allowed or invaled method"}), 405

@app.post("/account_verification")
async def verify_otp(request: Request):
    data = await request.json()
    enterd_otp = data.get("ENTERD_OTP")
    UID = data.get("UID")
    COOKIE = data.get("COOKIE")
    if UID and COOKIE:
        if enterd_otp == str(get.stored_otp(UID, COOKIE)):
            update.otp(0, UID, COOKIE)
            return {"message":"Email verified sucessfully", "TOKEN": get.token(COOKIE)},200
        else:
            return {"message": "Access Denaid ! Invalid otp"}, 401
    else:
        return {"message": "missing cookie or uid"}, 403






@app.get('/login')
def login_get(request: Request):
    return render_template("login.html"), 200
    

# if ussr logs in with mail password
@app.post("/login")
async def login(request: Request):
    PROVIDED_EMAIL = None
    PROVIDED_PASS = None
    STORED_PASSWORD = None
    all_emails = None
    data = None
    COOKIE = None
    UID = None
    otp = None
    if True:
        data = await request.json()
        PROVIDED_EMAIL = data.get("EMAIL")
        PROVIDED_PASS = data.get("PASSWORD")
        if PROVIDED_EMAIL and PROVIDED_PASS:
            all_emails = get.all_emails()
            if all_emails:
                if (f"{PROVIDED_EMAIL}",) in all_emails:
                    STORED_PASSWORD = get.password(PROVIDED_EMAIL)
                    if PROVIDED_PASS == STORED_PASSWORD:
                        COOKIE = get.cookie(PROVIDED_EMAIL)
                        UID = get.uid_by_email(PROVIDED_EMAIL)
                        otp = get.stored_otp(UID, COOKIE)
                        if len(str(otp)) == 1:
                            return {"message": "logged in sucessfully", "COOKIE": COOKIE, "UID": UID, "TOKEN": get.token(COOKIE)},200
                        else:
                            sendOTP(PROVIDED_EMAIL, otp, get.first_name(UID),"otpForNewAcc")
                            return {"message": "Access Denaid ! Verification pending", "redirect": True},401
                    else:
                        return {"message": "invalid password"},401
                else:
                    return {"message": "No account associated with provided account"}, 401
            else:
                return {"message":"Internal Server Err ;"}, 500
        else:
            return {"message":"Access Denaid ! Email or password missing"}, 401



## if user logs in with cookie
@app.post("/get_token")
async def return_token(request: Request):
    if True:
        data = await request.json()
        # for d in data:
        #     print(type(d))
        #     print(type(data))
        # return 
        PROVIDED_COOKIE = data.get("COOKIE")
        PROVIDED_UID = data.get("UID")
        # print(data)
        if PROVIDED_COOKIE and PROVIDED_UID:
            ORIGINAL_UID = get.uid_by_cookie(PROVIDED_COOKIE)
            if ORIGINAL_UID and ORIGINAL_UID == PROVIDED_UID:
                stored_otp = get.stored_otp(ORIGINAL_UID, PROVIDED_COOKIE)
              #  print(len(str(stored_otp)))
                # print(str(stored_otp))
                if len(str(stored_otp)) == 1:
                    return {"message":"Login sucess", "TOKEN": get.token(PROVIDED_COOKIE)}, 200
                else:
                    #sendOTP(get.email(PROVIDED_COOKIE),str(stored_otp), get.first_name(ORIGINAL_UID),"otpForNewAcc")
                    return {"message": "Verification pending"}, 409
            else:
                return {"message": "Access Denaid ! Login needed"}, 400
        else:
            return {"mesaage":"Access Denaid ! missing cookie or uid"}, 403
    # else:
    #     return {"message": "Access Denaid ! imvalid method"}, 405



@app.post("/get_all_users")
async def return_all_avilable_users(request: Request):
    if True:
        try:
            auth = await request.json()
            # print(auth)
            TOKEN = auth.get("TOKEN")
            UID = auth.get("UID")
            if TOKEN and UID:
                CURRECT_UID = get.uid_by_token(TOKEN)
                if CURRECT_UID == UID:
                    all_users_arr = get.all_users()
                   # print(all_users_arr, type(all_users_arr))
                    data = {}
                    if all_users_arr:
                        for user in all_users_arr:
                            data[user[2]]= {
                                "NAME": " ".join([user[0], user[1]])
                            }
                        return data
                    else:
                        return {"message":"unable fo fetch users"},404
                else:
                    return {"message": "Access Denid ! authentication faild"},401
            else:
                return {"message":" Accss Denaid ! login needed"},401
        except Exception as e:
            print('something went wrong', e)
            return {"message":"something went wrong"},401
    # else:
    #     return jsonify({"message":"method mot allowed"}),405

        
@app.post("/resend_otp")
async def resend_otp():
    if True:
        data = await request.json()
        print(data)
        COOKIE = data.get("COOKIE")
        UID = data.get("UID")
        MODE = data.get('MODE')
        if get.uid_by_cookie(COOKIE) == UID:
            if MODE and MODE == 'EMAIL_CHANGE':
                otp = generate_otp()
                email_change_otps_dict[UID] = otp
                EMAIL = data.get('EMAIL')
            else:
                otp = get.stored_otp(UID, COOKIE) 
                EMAIL = get.email(COOKIE)

            FIRST_NAME = get.first_name(UID)
            # print(otp)
            # print(EMAIL)
            # print(FIRST_NAME)
            if (EMAIL and otp and FIRST_NAME) or (EMAIL):
                otp_response = sendOTP(EMAIL, otp, FIRST_NAME,"otpForNewAcc")
                if otp_response.get("status_code") == 200:
                    return jsonify({"message": "OTP sent sucessfully"}),200
                elif otp_response.get("status_code") == 429:
                    return jsonify({"message": "Faild ! Too much requets wait amd retry after 20 minitus"}),429
                elif otp_response.get("status_code") == 400:
                    return jsonify({"message":"Plase check Email"}),400
                else:
                    return jsonify({"message":"Something went wrong", "otp_status": otp_response}), otp_response.get("status_code")
            else:
                return jsonify({"message":"unable to get data from database"}),501
        else:
            return jsonify({"mesaage": "authentication faild"}),401
    # else:
    #     return jsonify({"message":"method not allowed"}),405


@app.post("/get_old_messages")
async def get_old_messages(request: Request):
    if request.method == "POST":
        data = await request.json()
        COOKIE = data.get("COOKIE")
        UID = data.get("UID")
        if get.uid_by_cookie(COOKIE) == UID:
            limit = 30
            ## find all the chats of user
            all_chats_json = get.all_chats_json(UID)
            ## now get the message
            # print()
            # print()
            # print()
            # print()
            # print()
            # print()
            # print()
            # print(all_chats_json.keys())
            groups_messages = dict()
            for guid in all_chats_json.keys():
                all_messages_dict_type = get.all_messages_json(limit, guid)
                # now append to this group data on all group dict
                if all_messages_dict_type:
                    groups_messages[str(guid)] = all_messages_dict_type
                else:
                    print(f"err while getting data of group ==>> {guid} and err is {all_messages_dict_type}")
                    return {"message": "cant able to fetch old messages"}, 400
            #print(groups_messages)
            return {"message":"sucessfully got messags of all chats","groups_messages":groups_messages}, 200
        else:
            return {"message": "Access Denaid ! auth faild"}, 403






@app.post("/get_settings_data")
async def get_settings_data_post(request: Request):
    data = await request.json()
    print(data)
    if data and data.get('COOKIE'):
        users_stored_data = get.all_personal_data(data.get('UID'))
        print(users_stored_data)
        if users_stored_data:
            print(data.get('COOKIE'), users_stored_data.get('COOKIE'))
            if data.get('COOKIE') == users_stored_data.get('COOKIE'):
                print('user verified ') if is_developement else None
                return {"message": "Sucessfully got all details", 'credentials': users_stored_data}, 200
            else:
                return {'message': 'Authentication Faild weiredly'}, 400
        else:
            return {'message': 'Cant able find you account data'}, 400
    else:
        return {'message': 'some details are missing'}, 401
#     return jsonify({'message': "Access Denaid !!"}), 409
# )



@app.patch("/get_settings_data")
async def get_settings_data_patch(request: Request):
    data = await request.json()
    print(data)
    if data:
        users_stored_data = get.all_personal_data(data.get('UID'))
        if users_stored_data:
            if users_stored_data.get('EMAIL') == data.get('EMAIL'):
                if users_stored_data.get('PASSWORD') == data.get('PASSWORD'):
                    # details verification
                    update.personal_data(data)
                    return jsonify({'message':'sucessfully updated data'}), 200

                    ##### ill implement thse validations soon
                    FIRST_NAME_VALIDATION = validator.validate_first_name(data.get('FIRST_NAME'))
                    LAST_NAME_VALIDATION = validator.validate_last_name(data.get('LAST_NAME'))
                    EMAIL_VALIDATION = validator.validate_email(data.get('EMAIl'))
                    PHONE_NO_VALIDATION = validator.validate.phone_no(data.get('PHONE_NO'))
                    DOB_VALIDATION = validator.validate_dob(data.get('DOB'))
                    PROFILE_PIC_VALIDATION = validator.validate_profile_pic_url(data.get('PROFILE_PIC'))
                    try:
                        if  FIRST_NAME_VALIDATION and LAST_NAME_VALIDATION and EMAIL_VALIDATION and PHONE_NO_VALIDATION and DOB_VALIDATION and PROFILE_PIC_VALIDATION:
                            update.personal_data(data)
                            return jsonify({'message':'sucessfully updated data'}), 200
                    except Exception as e:
                            return jsonify({'message': e, }), 401
                else:
                    return jsonify({'message': 'Wrong Password please Retry With currect one'}), 401
            else:
                # is program control is hear then user has changed email
                # so verify new email only after that do
                if data.get('UID') in email_change_otps_dict:
                    if data.get('EMAIL') not in get.all_emails():
                        if email_change_otps_dict.get(data.get('UID')) == data.get('OTP'):
                            ## ill add updatee data part also 
                            return jsonify({'message':'sucessfully updated data'}), 200
                        else:
                            return jsonify({"message": " Can't change email !! incurrect OTP"})
                    else:
                        return jsonify({'message':'Provided Email already Associated with another account'}), 409
                else:
                    return jsonify({'message': 'feels like you have not sended otp till yet please click on send otp button and enter the sended OTP to verify your new Email'}), 403
        else:
           return jsonify({"message":"unable to reach your data please make sure you're not modified source"}), 403
    else:
        return jsonify({"message": " Missing request data "}), 409
# else:
#     return jsonify({'message': 'Method not supported'}), 501









# @app.route('/get_settings_data', methods=['POST', 'PATCH'])
# def get_settings_data():
#     if request.method == 'POST':
#         data = request.get_json()
#         print(data)
#         if data and data.get('COOKIE'):
#             users_stored_data = get.all_personal_data(data.get('UID'))
#             print(users_stored_data)
#             if users_stored_data:
#                 print(data.get('COOKIE'), users_stored_data.get('COOKIE'))
#                 if data.get('COOKIE') == users_stored_data.get('COOKIE'):
#                     print('user verified ') if is_developement else None
#                     return jsonify({"message": "Sucessfully got all details", 'credentials': users_stored_data}), 200
#                 else:
#                     return ({'message': 'Authentication Faild weiredly'}), 400
#             else:
#                 return jsonify({'message': 'Cant able find you account data'}), 400
#         else:
#             return jsonify({'message': 'some details are missing'}), 401
#         return jsonify({'message': "Access Denaid !!"}), 409
        
        
#     elif request.method == 'PATCH':
#         data = request.get_json()
#         print(data)
#         if data:
#             users_stored_data = get.all_personal_data(data.get('UID'))
#             if users_stored_data:
#                 if users_stored_data.get('EMAIL') == data.get('EMAIL'):
#                     if users_stored_data.get('PASSWORD') == data.get('PASSWORD'):
#                         # details verification
#                         update.personal_data(data)
#                         return jsonify({'message':'sucessfully updated data'}), 200
                        
                        
#                         ##### ill implement thse validations soon
#                         FIRST_NAME_VALIDATION = validator.validate_first_name(data.get('FIRST_NAME'))
#                         LAST_NAME_VALIDATION = validator.validate_last_name(data.get('LAST_NAME'))
#                         EMAIL_VALIDATION = validator.validate_email(data.get('EMAIl'))
#                         PHONE_NO_VALIDATION = validator.validate.phone_no(data.get('PHONE_NO'))
#                         DOB_VALIDATION = validator.validate_dob(data.get('DOB'))
#                         PROFILE_PIC_VALIDATION = validator.validate_profile_pic_url(data.get('PROFILE_PIC'))
#                         try:
#                             if  FIRST_NAME_VALIDATION and LAST_NAME_VALIDATION and EMAIL_VALIDATION and PHONE_NO_VALIDATION and DOB_VALIDATION and PROFILE_PIC_VALIDATION:
#                                 update.personal_data(data)
#                                 return jsonify({'message':'sucessfully updated data'}), 200
#                         except Exception as e:
#                                 return jsonify({'message': e, }), 401
#                     else:
#                         return jsonify({'message': 'Wrong Password please Retry With currect one'}), 401
#                 else:
#                     # is program control is hear then user has changed email
#                     # so verify new email only after that do
#                     if data.get('UID') in email_change_otps_dict:
#                         if data.get('EMAIL') not in get.all_emails():
#                             if email_change_otps_dict.get(data.get('UID')) == data.get('OTP'):
                                
#                                 ## ill add updatee data part also 
                                
#                                 return jsonify({'message':'sucessfully updated data'}), 200
#                             else:
#                                 return jsonify({"message": " Can't change email !! incurrect OTP"})
#                         else:
#                             return jsonify({'message':'Provided Email already Associated with another account'}), 409
#                     else:
#                         return jsonify({'message': 'feels like you have not sended otp till yet please click on send otp button and enter the sended OTP to verify your new Email'}), 403
#             else:
#                return jsonify({"message":"unable to reach your data please make sure you're not modified source"}), 403
#         else:
#             return jsonify({"message": " Missing request data "}), 409
#     else:
#         return jsonify({'message': 'Method not supported'}), 501


        
        
        
        
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
#         return jsonify({"message": f"User {user_id} ed group {group_id}"}), 200


#@socketio.on("connect_user")
# def show_user_connected(data):
def show_user_connected(data, ws):
    print(" new  user/clint has been connected ")
    
####################################################################################
####################################################################################
############################# SOCKET IO ROUTES/EVENTS ##############################
####################################################################################
####################################################################################

#@socketio.on("get_all_chat_list")
#def wants_all_his_chats(data):
def wants_all_his_chats(data, ws):
    # clint sends a json object im storing that json object on data variable
    # print(f"sended data from clint is =>>>>> {data}")
    PROVIDED_UID = data.get("UID")
    ACCESS_TOKEN = data.get("TOKEN")
    
    if not PROVIDED_UID or not ACCESS_TOKEN:
        return {"status_code": 401, "message": "accesToken or UID is missing"}
    
    ### compare the data UID and accessTokens are valid or not from database
    UID = get.uid_by_token(ACCESS_TOKEN)
    if UID == PROVIDED_UID:
        all_chats_json = get.all_chats_json(UID)
        # print(all_chats_json)
        # print(type(all_chats_json))
        
        # join the all groups
        # so that in send_messsage event rout can 
        # broadcast the message to that group and this usesr will able to lisen for new messaages
        for room_id in all_chats_json.keys():
            socketio.join_room(room_id, UID, ws)
            # print(type(room_id))
            print(f"user {UID} enterd in room {room_id}")
            
        if all_chats_json:
            return {"message":"Sucessfully Got Chats","status_code":200, "chats":all_chats_json}
        else:
            return {"mesaage":"Internal Server Err !", "status_code": 500}
    else:
        print("Access Denaid !")
        return {"status_code": 401, "message": "Access Denaid ! invalid token you need to login again"}


#@socketio.on("send_message")
#def send_message(data):
def send_message(data, ws):
    # print(data)
    sender_id = data.get("SENDER_ID")
    message = data.get("MESSAGE")
    group_id = data.get("GROUP_ID")
    profile_pic = data.get("PROFILE_PIC")
    
    sender_name = get.first_name(sender_id)
    if sender_id and message:
        # print(sender_id, message)
        message_id, time_stamp, profile_pic = write_in_database.store_this_message(group_id, sender_id, sender_name, message, profile_pic)
        
        # print(message_id, time_stamp)
        # socketio.emit("new_message", {
        #     "sender_id": sender_id,
        #     "sender_name": sender_name,
        #     "message": message,
        #     "group_id": group_id,
        #     "message_id": message_id,
        #     "time_stamp": time_stamp
        # }, ws, room=group_id)
        
        message_data = {
            "SENDER_ID": sender_id,
            "SENDER_NAME": sender_name,
            "MESSAGE": message,
            "GROUP_ID": group_id,
            "MESSAGE_ID": message_id,
            "TIME_STAMP": time_stamp,
            "PROFILE_PIC": profile_pic
        }
        
        return {"message": "message sent sucessfully", "content": message_data,"status_code":200}
        
        
##@socketio.on("send_message_new_chat")
#def send_message_new_chat(data):
def send_message_new_chat(data, ws):
    # print("this is new xhat",data)
    # sid = request.sid
    # print(type(rooms(sid)))
    sender_id = data.get("SENDER_ID")
    message = data.get("MESSAGE")
    group_id = data.get("GROUP_ID")
    reciever_id = group_id.rsplit("0000000000000000")[1]
    # print(group_id)
    # print(type(group_id))
    
    sender_name = get.first_name(sender_id)
    # if group_id not in rooms(sid):
    if group_id not in rooms.keys():
        socketio.join_room(group_id, sender_id, ws)
        # print("runnig first")
        #write in senders chat list
        write_in_database.add_user_in_group(sender_id, group_id, get.first_name(reciever_id) + " " + get.last_name(reciever_id))
        #write in recievers xhat list
        write_in_database.add_user_in_group(reciever_id, group_id, get.first_name(sender_id) + " " + get.last_name(sender_id))
        
    # write message and get the message_id and time_stamp
    message_id, time_stamp = write_in_database.store_this_message(group_id, sender_id, sender_name, message)
    if sender_id and message:
       # print(sender_id, message)
        # socketio.emit("new_message", {
        #     "sender_id": sender_id,
        #     "message": message,
        #     "group_id": group_id,
        #     "message_id": message_id,
        #     "time_stamp": time_stamp
        # },ws, room=group_id)
        
        message_data = {
            "SENDER_ID": sender_id,
            "MESSAGE": message,
            "GROUP_ID": group_id,
            "MESSAGE_ID": message_id,
            "TIME_STAMP": time_stamp
        }
        return {"message": "new message", "content": message_data,"status_code":200}

#################################₹##₹##₹###################№##
#################################₹##₹##₹###################№##
#######  USE THE flask-socks INSTED OF flask_socketIO  #######
#################################₹##₹##₹###################№##
#################################₹##₹##₹###################№##
@app.websocket("/ws")
async def websocket_handler(ws: WebSocket):
    await ws.accept()
    connected_clients.add(ws)
    try:
        while True:
            print("client connected", ws)

            # receive as text directly
            raw_text = await ws.receive_text()
            print("raw:", raw_text)

            try:
                msg = json.loads(raw_text)
                print(msg, type(msg))

                event = msg.get("event")
                data = msg.get("data")

                print('this is data ', data, type(data))
                ####### handle the events ########
                if event == "send_message":
                    print("called send_message")
                    result = await send_message(data, ws) if callable(send_message) and send_message.__code__.co_flags & 0x80 else send_message(data, ws)
                    await ws.send_json({"event": event, "data": result})

                elif event == "send_message_new_chat":
                    print("called send_message_new_chat")
                    result = await send_message_new_chat(data, ws) if callable(send_message_new_chat) and send_message_new_chat.__code__.co_flags & 0x80 else send_message_new_chat(data, ws)
                    await ws.send_json({"event": event, "data": result})

                elif event == "get_all_chat_list":
                    print("calling wants_all_his_chats")
                    result = await wants_all_his_chats(data, ws) if callable(wants_all_his_chats) and wants_all_his_chats.__code__.co_flags & 0x80 else wants_all_his_chats(data, ws)
                    await ws.send_json({"event": event, "data": result})

                elif event == "connect_user":
                    print("called show_user_connected")
                    result = await show_user_connected(data, ws) if callable(show_user_connected) and show_user_connected.__code__.co_flags & 0x80 else show_user_connected(data, ws)
                    await ws.send_json({"event": event, "data": result})

            except Exception as e:
                print("error:", e)

    except WebSocketDisconnect:
        print("Client disconnected:", ws)
    finally:
        connected_clients.remove(ws)
        

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  
    uvicorn.run(app, host="0.0.0.0", port=port)