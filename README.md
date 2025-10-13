# ACode Chat Backend API

This is a real-time chat application backend built using the **FastAPI** framework in Python. It provides RESTful endpoints for user authentication, account management, and real-time communication via **WebSockets**.

## ✨ Features

### User Authentication
- Sign up, Login (Email/Password or Cookie/UID)
- OTP-based email verification
- Password protection

### Real-Time Chat
- WebSocket handling for real-time messaging
- Fetch chat history (up to the last 30 messages)

### Data Management
- Access to user profile and chat data
- Profile and settings update functionality
- Database backup and push capabilities

<!-- 


* **User Authentication:** Sign up, Login (Email/Password or Cookie/UID).
* **Account Security:** OTP-based email verification and password protection.
* **Real-time Chat:** WebSocket handling for sending and receiving messages instantly.
* **Data Management:** Fetching all users, chats, and a limited history of old messages (last 30).
* **Settings/Profile Updates:** Patching user profile data (name, email, profile picture, etc.) with password and optional email OTP verification.
* **CORS Enabled:** Configured for cross-origin requests (currently set to `*` for development).
* **Database Integration:** Uses custom modules (`API/DATABASE/`) suggesting integration with an SQLite database.
* **Database Backup/Push:** Includes an endpoint to trigger a push of database changes to a repository.
 -->
---

## ToDo

- [x] signup
- [x] signin
- [x] verification
- [x] public api
- [] strict security
- []  ORM implementation
- []  data hashing
- []  route protection
- []  rate limitation
- []  attack protection


<!-- ## LICENCE

this repository is `MIT LICENCED` and anyone can able to modify/reuse it for his projects
 -->


 ## License
 This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🚀 Setup and Installation

### Prerequisites

* Python 3.x
* The required Python libraries (FastAPI, uvicorn, Jinja2, etc.)
* Custom modules (e.g., `API.GENERAL.*`, `API.DATABASE.*`, `GLOBAL_DATABASE_API.*`) must be present in the project structure everything runs through these files.

### 1. Clone the Repository

```bash
git clone https://github.com/hackesofice/Acode-Chat-Backend.git>
cd acode-chat-backend
```

### 2. Install Dependencies
You'll need to install FastAPI, Uvicorn, and Starlette, or simply install through given cmd
```
pip install fastapi uvicorn python-multipart jinja2 python-jose python-dotenv starlette
```
OR
```
pip install -r requirements.txt
```
> Note: Ensure your custom modules (e.g., API/GENERAL/cookie.py, API/DATABASE/get_data.py, etc.) are correctly placed and configured.

### 3. Run the Application

start the application using the given cmd.

```
python main.py
```

The API will be available at http://0.0.0.0:22148.

# 🗺️ API Endpoints Reference

### Authentication & Account
|        Path      	|        Method         |                	  Description                                    |     	Status Codes         |
|-------------------|-----------------------|--------------------------------------------------------------------|---------------------------|
|/sign_up	        |        POST	        |    Registers a new user and sends an OTP for verification.         |	  200, 400, 409, 429     | 
|/account_verification|    	POST	        |    Verifies a new user account using the sent OTP.	             |    200, 401, 403          |
|/login	            |        POST	        |    Authenticates user with email/password. May trigger OTP resend if unverified.|	200, 401, 403|
|/get_token	        |        POST	        |    Authenticates user using an existing COOKIE and UID (session refresh).	|     200, 401, 403, 422|
|/resend_otp	    |        POST	        |    Resends the verification OTP. Supports normal verification or email change mode.|	200, 401, 409, 429|
|/get_settings_data	|        POST	        |    Retrieves the authenticated user's profile and settings data.	|200, 400, 401 |
|/get_settings_data	|        PATCH	        |    Updates user profile data (requires password/OTP for sensitive changes).|	200, 401, 403, 409 |
|/get_profile_pic_link/{uid}|	GET	        |    Retrieves the profile picture URL for a specific user ID.|	200|


 
### Chat Data & Utilities



|Path                |                    Method                    |                Description                                                |    Status Codes     |
|--------------------|----------------------------------------------|---------------------------------------------------------------------------|---------------------|
| /get_all_users	 |                    POST	                    |    Fetches a dictionary of all available users in the system.	            |    200, 401, 404    |
| /get_all_chats     |                    POST	                    |    Fetches a list of all chats (groups/conversations) a user belongs to.	|    200, 403, 404    |
| /get_old_messages	 |                    POST	                    |    Fetches the last 30 messages for all of the user's chats.	            |    200, 400, 403
| /uptime	         |                    GET	                    |    Checks if the API is running.	                                        |    200
| /quick_quick_save_data_to_database_repository|	GET	            |    Manually triggers a database push/backup operation.	                |    200



# 💬 Real-Time Communication (WebSockets)

The application uses a WebSocket connection for real-time messaging, managed by the custom SocketManager.

### WebSocket Endpoint

Connect to the WebSocket at: `ws://<API-HOST>/ws/{client_id}`

|            Event (Client Sends)	             |                       Description	                |                                                            Server Action                                                      | 
|------------------------------------------------|------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
|    wants_all_his_chats	                     |    Sent on initial connection/authentication.	    |    Server verifies token, joins the client to all their existing chat rooms, and sends back the list of chats.                |
|        send_message	                         |    Sent when a user types and sends a message.	    |    Server stores the message in the database, sends the complete message object back to the sender, and broadcasts it to all other clients in the specified GROUP_ID room.|


### Data Structure for send_message (Client to Server)

```JSON

{
    "event": "send_message",
    "data": {
        "SENDER_ID": "user_id_int",
        "MESSAGE": "the chat content",
        "GROUP_ID": "group_id_str",
        "PROFILE_PIC": "url_to_profile_pic"
    }
}

```

### Data Structure for Broadcasted Message (Server to Client)

The server broadcasts the full message details, including the newly generated database IDs and timestamps.

```JSON

{
    "event": "send_message",
    "data": {
        "SENDER_ID": "user_id_int",
        "SENDER_NAME": "Firstname Lastname",
        "MESSAGE": "the chat content",
        "GROUP_ID": "group_id_str",
        "MESSAGE_ID": "newly_created_message_id",
        "TIME_STAMP": "timestamp_of_message",
        "PROFILE_PIC": "url_to_profile_pic"
    }
}
```

# ⚙️ Development Notes 

**Custom Imports**: The functionality heavily relies on custom local modules (e.g., `API/GENERAL/*, API/DATABASE/*`).

**Security**: The application uses simple string comparison for password checks (`if PROVIDED_PASS == STORED_PASSWORD:`).

**CORS**: `allow_origins=["*"]` is set for development. Restrict this to your client application's domain(s) in production.

**OTP Verification**: The verification check relies on the length of the stored OTP (`if len(str(otp)) == 1:`), where `0` or `1` indicates verification, and a 6-digit number indicates pending verification.