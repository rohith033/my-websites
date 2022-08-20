from fastapi import FastAPI,WebSocket,WebSocketDisconnect
from sqlite3 import connect
from typing import List

from blog import  models
from datetime import datetime 
import json
from fastapi.middleware.cors import CORSMiddleware
from blog.database import engine
from blog.routers import blog, user, authentication
from locale import currency
from multiprocessing import managers
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)



