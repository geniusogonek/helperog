import sys
import speech_recognition
import webbrowser
import time

import os

from dotenv import load_dotenv
from playsound import playsound
from gtts import gTTS
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
from database.database import Database


load_dotenv()


TOKEN = os.getenv("TOKEN")
AVALIABLE = set(map(str, range(10))) | {"*", "+", "/", "-", "."}


gigachat = GigaChat(
    credentials=TOKEN,
    scope="GIGACHAT_API_PERS",
    model="GigaChat",
    verify_ssl_certs=False,
    streaming=False,
)

messages = [
    SystemMessage(
        content="Ты голосовой помощник, старайся отвечать кратко и по делу"
    )
]


def check_str(text):
    symbs = set(text)
    if AVALIABLE.intersection(symbs) == symbs:
        return True
    return False


def say(text):
    obj = gTTS(text, slow=False, lang="ru")
    obj.save("src/text.mp3")
    playsound("src/text.mp3")


sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5


def listening(self):
    """Функция прослушивания"""
    db = Database()
    db.init_tables()
    while True:
        if self.state == 1:
            with speech_recognition.Microphone(self.micro) as mic:
                sr.adjust_for_ambient_noise(mic, duration=0.5)
                data = sr.listen(mic)

            try:
                text = sr.recognize_google(data, language="ru").lower().replace("х", "*")
                start = time.time()
            except speech_recognition.exceptions.UnknownValueError:
                end = time.time()
                if end - start > 10:
                    self.listen_handler()
                continue

            if text in ["привет", "hi"]:
                say("Здравствуйте")

            elif text in ["открой youtube", "open youtube"]:
                webbrowser.open("https://youtube.com")
                say("Выполнено")
                db.add_request(text, "Выполнено")

            elif text in ["выключись", "turn off"]:
                say("Выключаюсь")
                db.add_request(text, "Выключаюсь")
                self.stop_handler()
                sys.exit()

            elif text in ["повтори", "repeat"]:
                last_saied = db.get_last_request()
                say(last_saied[1])

            elif text:
                print(text)
                last_num = db.get_last_num()[0]
                text = text\
                    .replace(",", ".")\
                    .replace("в степени", "**")\
                    .replace(" ", "")\
                    .replace("последняя", last_num)\
                    .replace("последние", last_num)

                if check_str(text):
                        num = str(eval(text))
                        say(num)
                        db.add_request(text, num, True)

                else:
                    messages.append(HumanMessage(content=text))
                    res = gigachat.invoke(messages)
                    messages.append(res)
                    say(res.content)
                    db.add_request(text, res.content)

            if self.stop == 1:
                sys.exit()