import sys
import speech_recognition
import webbrowser
import time

from playsound import playsound
from gtts import gTTS
from database.database import Database
from utils.elsetextcommand import elsetext


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
                text = sr.recognize_google(data, language="ru").lower()
                start = time.time()
            except speech_recognition.exceptions.UnknownValueError:
                end = time.time()
                try:
                    if end - start > 10:
                        self.listen_handler()
                except UnboundLocalError:
                    pass
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
                request, answer, is_num = elsetext(text)
                if is_num is not None:
                    db.add_request(request, answer, is_num)
                say(answer)

        if self.stop == 1:
            sys.exit()