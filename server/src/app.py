from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
# from fastapi.templating import Jinja2Templates
from src.database.connections import db_get_connections, db_create_connection
from src.database.db_connection import conn

security = HTTPBasic()
app = FastAPI(dependencies=[Depends(security)])
# templates = Jinja2Templates(directory="templates")

class Connection(BaseModel):
    value: str

users = {
    "admin": {
        "password": "changeme",
    }
}


def verification(creds: HTTPBasicCredentials = Depends(security)):
    username = creds.username
    password = creds.password
    if username in users and password == users[username]["password"]:
        print("User Validated")
        return True
    else:
        # From FastAPI 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )

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
                id serial primary key,
                name text,
                university_identification_number integer,
                connection_time timestamp DEFAULT current_timestamp
            )
        """

        await cursor.execute(q)


@app.get("/connections")
async def getConnections(Verification = Depends(verification)):
    if Verification:
        results = await db_get_connections()
        return {"code": 200, "data": results}
    else:
        return {"code": 401, "message": "Unauthorized"}

@app.post("/connect")
async def saveBluetoothConnection(connection: Connection, Verification = Depends(verification)):
    print("Data: ", connection)
    conn_split = connection.value.split(' ')
    data = {
        "name": conn_split[0],
        "university_identification_number": int(conn_split[1])
    }
    if(Verification):
        results = await db_create_connection(data)
        return {"code": 200, "data": results}
    else:
        return {"code": 401, "message": "Unauthorized"}


@app.get("/ping")
async def ping():
    return {"pong": "ok"}
