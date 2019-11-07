import pyttsx3
import speech_recognition as sr
import os
from fuzzywuzzy import fuzz
import datetime
import convert
import time
import weather
import timer
import calc
import win32com.client as wincl
import browser
import translate
import time
import anekdot
import browser_find
import cinemaParserModule as cpm


opts = {"alias": ('подручный', 'подручные', 'поручень', 'подручник', 'рука',''),
        "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси', 'как','сколько','поставь','переведи', "засеки",'запусти','сколько будет'),
        "cmds":
            {"ctime": ('текущее время', 'сейчас времени', 'который час', 'время'),
             "timer": ('таймер', 'таймер на', 'сек', 'мин'),
             "findFilms":("афиша", "лента", "кино", "афиша в", "кино в", "континент", "современник"),
             "findFilmInfoInCinema":("информация о", "сеанс фильма", "сеансы фильма", "стоимость сеанса", "фильм", "сеанс", "континент", "современник"),
             'startStopwatch': ('запусти секундомер', "включи секундомер", "начини"),
             'stopStopwatch': ('останови секундомер', "выключи секундомер", "прекрати"),
             "stupid1": ('расскажи анекдот', 'рассмеши меня', 'ты знаешь анекдоты', "шутка"),
             "calc": ('прибавить','умножить','разделить','степен','вычесть','поделить','х','+','-','/'),
             "shutdown": ('выключи', 'выключить', 'отключение', 'отключи', 'выключи компьютер'),
             "conv": ("валюта", "конвертер","доллар",'руб','евро'),
             "weather": ("погода", "погода в"),
             "internet": ("открой", "вк", "гугл", "сайт", 'вконтакте', "ютуб"),
             "translator": ("переводчик","translate"),
             "deals": ("дела","делишки", 'сам'),
             "find": ("найди", "поищи", "поиск в google", "google", "find", "поиск в гугле", "find in google")}}

startTime = 0
speak_engine = pyttsx3.init()
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[2].id)
r = sr.Recognizer()
m = sr.Microphone(device_index=1)
voice = "str"

#def play_mp3(filename):
#    pygame.mixer.init()
#    pygame.mixer.music.load(filename)
#    pygame.mixer.music.play()
#    while pygame.mixer.music.get_busy():
#        pygame.time.Clock().tick(10)
#    pygame.mixer.quit()

def speak(what):
     print(what)
     speak = wincl.Dispatch("SAPI.SpVoice")
     speak.Speak(what)


# def speak(phrase):
#     print(phrase)
#     tts = gTTS(text=phrase, lang="ru")
#     with tempfile.NamedTemporaryFile(suffix='.mp3', delete=True) as f:
#         tmpfile = f.name
#     tts.save(tmpfile)
#     play_mp3(tmpfile)

def callback(recognizer, audio):
    try:
        global voice
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()

        print("[log] Распознано: " + voice)

        if voice.startswith(opts["alias"]):
            cmd = voice

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()
            voice = cmd
            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])


    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")

def listen():
    with m as source:
        r.adjust_for_ambient_noise(source)
    stop_listening = r.listen_in_background(m, callback)
    while True: time.sleep(0.1)

def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    return RC

def execute_cmd(cmd):
    global startTime
    if cmd == 'ctime':
        now = datetime.datetime.now()
        speak("Сейчас {0}:{1}".format(str(now.hour), str(now.minute)))
    elif cmd == "findFilmInfoInCinema":
        cpm.cinemaParser(cmd)
    elif cmd == "findFilms":
        cpm.cinemaParser(cmd)
    elif cmd == 'timer':
        timer.time_r()
    elif cmd == 'shutdown':
        os.system('shutdown -s')
        speak("Выключаю...")
    elif cmd == 'calc':
        calc.calculator()
    elif cmd == 'weather':
        weather.check_weather()
    elif cmd == 'conv':
        convert.convertation()
    elif cmd == 'translator':
        translate.translate()
    elif cmd == 'stupid1':
        anekdot.fun()
    elif cmd == 'internet':
        browser.browser()
    elif cmd == 'startStopwatch':
        speak("Секундомер запущен")
        startTime = time.time()
    elif cmd == "find":
        browser_find.google_find()
    elif cmd == "stopStopwatch":
        if startTime != 0:
            Time = time.time() - startTime
            speak(f"Прошло {round(Time // 3600)} часов {round(Time // 60)} минут {round(Time % 60, 2)} секунд")
            startTime = 0
        else:
            speak("Секундомер не включен")
    elif cmd == 'deals':
        speak("Голова пока цела. Я имею ввиду процессор.")
    else:
        print("Команда не распознана")
