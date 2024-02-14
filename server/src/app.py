from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from src.database.connections import db_get_connections, db_create_connection, remove_record
from src.database.db_connection import conn

security = HTTPBasic()
app = FastAPI(dependencies=[Depends(security)])
app.mount("/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")

class Connection(BaseModel):
    value: str = Field(pattern=r'^[\w\s]+\s\d{3}-\d{4}$')

users = {
    "admin": {
        "password": "changeme",
    }
}


def verification(creds: HTTPBasicCredentials = Depends(security)):
    print()
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
                university_identification_number text,
                connection_time timestamp DEFAULT current_timestamp
            )
        """

        await cursor.execute(q)


@app.get("/connections")
async def get_connections(Verification = Depends(verification)):
    if Verification:
        results = await db_get_connections()
        return {"code": 200, "data": results}
    else:
        return {"code": 401, "message": "Unauthorized"}

@app.post("/connect")
async def save_bluetooth_connection(connection: Connection, Verification = Depends(verification)):
    conn_split = connection.value.split()
    data = {
        "name": " ".join(conn_split[:-1]),
        "university_identification_number": conn_split[-1]
    }
    if(Verification):
        results = await db_create_connection(data)
        return {"code": 200, "data": results}
    else:
        return {"code": 401, "message": "Unauthorized"}


@app.get("/records")
async def get_records(request: Request, Verification = Depends(verification)):
    results = await db_get_connections()
    return templates.TemplateResponse(
        request=request, name="table.html", context={"items": results or []}
    )

@app.delete("/remove/{record_id}")
async def delete_record(record_id: int, Verification = Depends(verification)):
    await remove_record(record_id)

    return 200





@app.get("/ping")
async def ping():
    return {"pong": "ok"}
