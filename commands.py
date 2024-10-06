import speech_recognition
import webbrowser

from playsound import playsound
from gtts import gTTS

AVALIABLE = set(map(str, range(10))) | {"*", "+", "/", "-"}


def check_str(text):
    symbs = set(text.replace(" ", "").replace("встепени", "**"))
    if AVALIABLE.intersection(symbs) == symbs:
        return True
    return False


def create_number(num):
    obj = gTTS(num, slow=False, lang="ru")
    obj.save("number.mp3")


sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5


def listening(self):
    with speech_recognition.Microphone() as mic:
        while True:
            if self.state == 1:
                sr.adjust_for_ambient_noise(mic, duration=0.5)
                data = sr.listen(mic)


                try:
                    text = sr.recognize_google(data, language="ru").lower().replace("х", "*")
                except speech_recognition.exceptions.UnknownValueError:
                    self.listen_handler()
                    continue

                if text == "привет":
                    playsound("Здравствуйте!.mp3")
                elif text == "открой youtube":
                    webbrowser.open("https://youtube.com")
                    playsound("Выполнено!.mp3")
                elif text == "выключись":
                    playsound("Обрабатываю.mp3")
                    exit()
                elif check_str(text) and text != "":
                    num = str(eval(text.replace("в степени", "**")))
                    create_number(num)
                    playsound("number.mp3")
                else:
                    return "Фраза не распознана: " + text
            else:
                print("state = 0")