import asyncio

import uvicorn

from fastapi import FastAPI
from fastapi.responses import Response, PlainTextResponse
from fastapi.requests import Request
from database.database import Database
from pydantic import BaseModel
from jwt_utils import decode_jwt, generate_jwt
from langchain_gigachat import GigaChat
from langchain_core.messages import HumanMessage, SystemMessage
from config import GIGACHAT_TOKEN


class AuthData(BaseModel):
    username: str
    password: str


llm = GigaChat(
    credentials=GIGACHAT_TOKEN,
    scope="GIGACHAT_API_PERS",
    model="GigaChat",
    verify_ssl_certs=False,
    streaming=False,
)

messages = [
    SystemMessage(
        content="Ты эмпатичный бот-психолог, который помогает пользователю решить его проблемы."
    )
]


app = FastAPI()
db = Database()


@app.post("/login")
async def login(data: AuthData):
    if db.login_user(data.username, data.password):
        return generate_jwt(data)
    return


@app.post("/register")
async def register(data: AuthData):
    if db.register_user(data.username, data.password):
        jwt_token = generate_jwt(data)
        response = Response(jwt_token)
        response.set_cookie("Authorization", jwt_token)
        return response
    return


@app.get("/gigachat", response_class=PlainTextResponse)
async def gigachat(request: Request, question):
    jwt_token = request.cookies.get("Authorization")
    if validate(jwt_token):
        username = decode_jwt(jwt_token).get("username")
        if db.get_token_used(decode_jwt(username)) < 49500:
            answer = get_answer(question)
            db.increase_token_used(username, len(answer))
            return answer
        return "Вы истратили свой запас токенов!"
    return "Вы не авторизованы!"


def get_answer(question):
    answer = llm.invoke(messages + [HumanMessage(question)])
    return answer.content


def validate(jwt_token):
    data = decode_jwt(jwt_token)
    if data is not None:
        return db.login_user(data["username"], data["password"])
    return False


async def main():
    db.create_tables()
    server = uvicorn.Server(uvicorn.Config(app))
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())