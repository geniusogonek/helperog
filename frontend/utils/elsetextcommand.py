import os

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
from database.database import Database
from requests import Session
from http.cookiejar import LWPCookieJar


with open("frontend/token.txt", "r") as file:
    TOKEN = file.read()

AVALIABLE = set(map(str, range(10))) | set("*+/-.()")


gigachat = GigaChat(
    credentials=TOKEN,
    scope="GIGACHAT_API_PERS",
    model="GigaChat",
    verify_ssl_certs=False,
    streaming=False,
) if TOKEN != "" else None

db = Database()
db.close_connection()


def load_cookies(session, filename):
    lwpc_jar = LWPCookieJar()
    lwpc_jar.load(filename, ignore_discard=True, ignore_expires=True)
    session.cookies.update(lwpc_jar)

session = Session()
if os.path.exists("cookies.txt"):
    load_cookies(session, "cookies.txt")

messages = [
    SystemMessage(
        content="Ты голосовой помощник, старайся отвечать кратко и по делу"
    )
]


def check_str(text):
    symbs = set(text)
    return AVALIABLE.intersection(symbs) == symbs


def elsetext(text):
    db.reopen_connection()
    last_num = db.get_last_num()[0]
    db.close_connection()
    new_text = text\
        .replace("х", "*")\
        .replace(",", ".")\
        .replace("в степени", "**")\
        .replace(" ", "")\
        .replace("последняя", last_num)\
        .replace("последние", last_num)

    if check_str(new_text):
            num = str(eval(new_text))
            return new_text, num, True

    elif gigachat is not None:
        messages.append(HumanMessage(content=text))
        res = gigachat.invoke(messages)
        messages.append(res)
        return text, res.content, False
    else:
        message = session.get("http://127.0.0.1:8000/gigachat", params={"question": text})
        return text, message.text, False