from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
import asyncio
from game_engine import GameEngine

app = FastAPI()
engine = GameEngine()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections.copy():
            try:
                await connection.send_json(message)
            except Exception:
                self.disconnect(connection)

manager = ConnectionManager()
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(engine.run_game_loop(manager))
@app.websocket("/ws/game")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            engine.process_input(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)