from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit
import sqlite3, random, string

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def db_conn():
    return sqlite3.connect("local.db")

def generate_id():
    return str(random.randint(100000000, 9999999999))

def generate_cookie():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=64))

def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

@app.route("/")
def home():
    return "API is Alive"

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

@app.route("/get_messages", methods=["POST"])
def get_messages():
    thread_id = request.form.get("thread_id")
    user_id = request.form.get("user_id")
    cookie = request.form.get("cookie")

    with db_conn() as conn:
        cur = conn.execute("SELECT cookie FROM users WHERE id=?", (user_id,))
        row = cur.fetchone()
        if not row or row[0] != cookie:
            return jsonify({"message": "Invalid user"}), 401

        messages = conn.execute(
            "SELECT sender_id, sender_name, message, timestamp FROM messages WHERE thread_id=? ORDER BY timestamp ASC",
            (thread_id,)
        ).fetchall()

        return jsonify([
            {
                "sender_id": msg[0],
                "sender_name": msg[1],
                "message": msg[2],
                "timestamp": msg[3]
            }
            for msg in messages
        ])

@app.route("/get_groups", methods=["POST"])
def get_user_groups():
    user_id = request.form.get("user_id")
    cookie = request.form.get("cookie")

    with db_conn() as conn:
        cur = conn.execute("SELECT cookie FROM users WHERE id=?", (user_id,))
        row = cur.fetchone()
        if not row or row[0] != cookie:
            return jsonify({"message": "Invalid session"}), 401

        groups = conn.execute(
            "SELECT group_id FROM user_groups WHERE user_id=?",
            (user_id,)
        ).fetchall()

        return jsonify([g[0] for g in groups])



@socketio.on("connect_user")
def handle_user_connect(data):
    user_id = data.get("user_id")
    cookie = data.get("cookie")

    with db_conn() as conn:
        cur = conn.execute("SELECT cookie FROM users WHERE id=?", (user_id,))
        row = cur.fetchone()
        if not row or row[0] != cookie:
            emit("error", {"message": "Invalid session"})
            return

        groups = conn.execute("SELECT group_id FROM user_groups WHERE user_id=?", (user_id,)).fetchall()
        for (group_id,) in groups:
            join_room(group_id)
        emit("connected", {"joined_rooms": [g[0] for g in groups]})


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
    socketio.run(app, port=5000, host="0.0.0.0", debug=True)
