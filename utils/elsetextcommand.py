from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
from database.database import Database


with open("token.txt", "r") as file:
    TOKEN = file.read()

AVALIABLE = set(map(str, range(10))) | set("*+/-.()")


gigachat = GigaChat(
    credentials=TOKEN,
    scope="GIGACHAT_API_PERS",
    model="GigaChat",
    verify_ssl_certs=False,
    streaming=False,
) if TOKEN is not None else None

db = Database()


messages = [
    SystemMessage(
        content="Ты голосовой помощник, старайся отвечать кратко и по делу"
    )
]


def check_str(text):
    symbs = set(text)
    return AVALIABLE.intersection(symbs) == symbs



def elsetext(text):
    last_num = db.get_last_num()[0]
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
        return "Сначала установите токен", None, None