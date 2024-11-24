import asyncio

import uvicorn

from fastapi import FastAPI
from database import Database
from pydantic import BaseModel
from jwt_utils import decode_jwt, generate_jwt


class AuthData(BaseModel):
    username: str
    password: str


app = FastAPI()
db = Database()


@app.post("/login")
async def login(data: AuthData):
    if db.login_user(data.username, data.password):
        return generate_jwt(data)


@app.post("/register")
async def register(data: AuthData):
    if db.register_user(data.username, data.password):
        return generate_jwt(data)


def validate(jwt_token):
    data = decode_jwt(jwt_token)
    return db.login_user(data["username"], data["password"])


async def main():
    db.create_tables()
    server = uvicorn.Server(uvicorn.Config(app))
    await server.server()