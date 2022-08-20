from fastapi import FastAPI,WebSocket,WebSocketDisconnect,APIRouter
from sqlite3 import connect
from typing import List
from blog import  models
from datetime import datetime 
import json
from blog.database import engine
# from blog.repository import mess
from locale import currency
from multiprocessing import managers
router = APIRouter(
    prefix="/blog",
    tags=['Blogs']
)
class connectionManager:

    def __init__(self) -> None:
        self.active_connection: List[WebSocket] = []
    async def connect(self,websocket:WebSocket):
        await websocket.accept()
        self.active_connection.append(websocket)
    def disconnect(self,websocket:WebSocket):
        self.active_connection.remove(websocket)
    # sending message to a specific websocket
    async def send_to_user(self, message:str,websocket:WebSocket):
        await websocket.send_txt(message)
    # broadcasting to the whole network of websocket
    async def broadcast(self,message:str):
        for i in self.active_connection:
           await i.send_txt(message)
Manager = connectionManager()
models.Base.metadata.create_all(engine)
@router.put('/{id}')
async def socket_end(websocket: WebSocket ,id:int):
    await Manager.connect(websocket)
    now = datetime.now()
    cur_time = now.strftime("%H:%M")
    try:
        while True:
            data = await websocket.rceive_text()
            message = {'time':cur_time,'id':id,'message':data}
            await Manager.broadcast(json.dumps(message))
    except WebSocketDisconnect:
        Manager.disconnect(websocket)
        message = {'time':cur_time,'id':id,'message':"offline"}
        await Manager.broadcast(json.dumps(message))