from types import CodeType
from fastapi import WebSocket


class SocketManager:
    """ IT MANAGES THE MESSAGE SENDING PROCESS LIKE BROADCASTING """

    def __init__(self, all_online_users):
        self.all_online_users = all_online_users
        self.__rooms = dict()  #for storing all rooms and its an nested dict

    def emit(self, event: str, data: dict, ws: WebSocket, room: int | str):
        """ Sends the message to specific chat group"""
        if (room in self.__rooms) and (ws in self.__rooms[room].values()):
            for uid, wss in self.__rooms[room].items():
                if uid == data["UID"]:
                    continue
                wss.send_jsomn({"event": event, "data": data})

    def join_room(self, room_id: str, user_id: str, ws: str):
        """ adds user to an group for listenong messages """
        self.__rooms.setdefault(str(room_id), {})[str(user_id)] = str(ws)
        return True

    def leave_room(self, user_id: str, room_id: str):
        """ MAINLY DESIGNED FOR WHEN USER LEAVES AN GROUP CHAT """
        self.__rooms[room_id].remove(user_id) if self.__rooms.get(
            room_id) else print(
                'user not avilable in rooms skipped message sending')
        return True

    def leave_rooms(self, user_id: str):
        """ REMOVES USER FROM ALL GROUPS MAINLY DESIGNED FOR OFFLINE, WHEN USER GOES OFFLINE """
        for room in self.__rooms:
            for uid in self.__rooms[room]:
                if uid == user_id:
                    self.__rooms[room].remove(uid)
        return True

    def broadCastMessage(self, message, type: CodeType | str):
        """ Designed for any important notice by application admin to broadcast in all connected users """
        for ws in self.all_online_users:
            ws.send({
                "event": "application_admin",
                "type": type,
                "data": {
                    "message": message
                }
            })
