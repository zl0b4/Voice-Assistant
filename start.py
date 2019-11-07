import funcs
import time
import datetime


now = datetime.datetime.now()

if now.hour >= 6 and now.hour < 12:
    funcs.speak("Доброе утро!")
elif now.hour >= 12 and now.hour < 18:
    funcs.speak("Добрый день!")
elif now.hour >= 18 and now.hour < 23:
    funcs.speak("Добрый вечер!")
else:
    funcs.speak("Доброй ночи!")

funcs.listen()
