import sys
import speech_recognition
import webbrowser
import time

from playsound import playsound
from gtts import gTTS
from database import add_request, get_last_request, init_tables


AVALIABLE = set(map(str, range(10))) | {"*", "+", "/", "-", "."}


def check_str(text):
    symbs = set(text.replace(" ", "").replace("встепени", "**"))
    if AVALIABLE.intersection(symbs) == symbs:
        return True
    return False


def create_number(num):
    obj = gTTS(num, slow=False, lang="ru")
    obj.save("src/number.mp3")


sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5


def listening(self):
    init_tables()
    with speech_recognition.Microphone() as mic:
        while True:
            if self.state == 1:
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

                if text == "привет":
                    playsound("src/Здравствуйте!.mp3")
                elif text == "добавить":
                    add_request("добавить", "добавлено")
                elif text == "тест":
                    print(get_last_request())
                elif text == "открой youtube":
                    webbrowser.open("https://youtube.com")
                    playsound("src/Выполнено!.mp3")
                elif text == "выключись":
                    playsound("src/Обрабатываю.mp3")
                    self.stop_handler()
                    sys.exit()
                elif check_str(text.replace(",", ".")) and text != "":
                    num = str(eval(text.replace("в степени", "**").replace(",", ".")))
                    create_number(num)
                    playsound("src/number.mp3")
                else:
                    print("Фраза не распознана: " + text)
            if self.stop == 1:
                sys.exit()