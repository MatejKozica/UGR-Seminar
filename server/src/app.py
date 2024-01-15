from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.database.connections import db_get_connections, db_create_connection
from src.database.db_connection import conn

app = FastAPI()

origins = ['http://localhost']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    async with conn.cursor() as cursor:
        q = """
            CREATE TABLE IF NOT EXISTS connections(
                id serial primary key
                mac_address macaddr
                name text
                connection_time timestamp DEFAULT current_timestamp
            )
        """

        await cursor.execute(q)


@app.get("/connections")
async def getConnections():
    results = db_get_connections()
    return {"code": 200, "data": results}

@app.post("/connect")
async def saveBluetoothConnection(macAddress, name):
    results = await db_create_connection({macAddress, name})
    return {"code": 200, "data": results}


@app.get("/ping")
async def ping():
    return {"pong": "ok"}