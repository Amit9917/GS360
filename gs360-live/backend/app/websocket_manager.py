from collections import defaultdict

from fastapi import WebSocket


class WebSocketManager:
    def __init__(self):
        self.rooms: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(self, user_id: str, ws: WebSocket):
        await ws.accept()
        self.rooms[user_id].append(ws)

    def disconnect(self, user_id: str, ws: WebSocket):
        if ws in self.rooms[user_id]:
            self.rooms[user_id].remove(ws)

    async def send_user(self, user_id: str, message: dict):
        for ws in list(self.rooms[user_id]):
            await ws.send_json(message)
