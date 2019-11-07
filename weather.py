import pyowm
import funcs
def check_weather():
    file = open('cities.txt')
    rl = file.readlines()
    owm = pyowm.OWM('b567af6828fb0dc81c822f00e7371439')
    if len(funcs.voice.split()) == 1:
        city = 'Магнитогорск'
    else:
        weather = funcs.voice.split()[-1].capitalize()
        if ''.join(list((weather[-2],weather[-1]))) == 'ом':
            weather = weather[:-2]
            weather += 'е'
        letters = ['\n', 'я\n', 'а\n', 'ь\n', 'й\n', 'о\n','ый\n','ий\n']
        if weather[-1] in 'еи':
            city_list = [weather.replace(weather[-1],letter) for letter in letters]
            while city_list:
                for i in city_list:
                    if i in rl:
                        city = i.strip()
                        city_list.clear()
                        break
                    else:
                        city_list.remove(i)
        else:
            city = weather

    try:
        observation = owm.weather_at_place(city)
        w = observation.get_weather()
        temperature = w.get_temperature('celsius')['temp']
        temp_max, temp_min = w.get_temperature('celsius')['temp_max'], w.get_temperature('celsius')['temp_min']
        wind_speed = w.get_wind()['speed']
        rain,snow = w.get_rain(),w.get_snow()

        if rain:
            funcs.speak("Сегодня будет дождь, возьмите зонт!")
        if snow:
            funcs.speak("Сегодня будет снег, оденьтесь потеплее")

        funcs.speak("В городе {0} температура {1} градусов по Цельсию. Скорость ветра {2} метра в секунду.".format(city,str(temperature),wind_speed))
        funcs.speak("Температура поднимется до {0} градусов и опустится до {1} градусов".format(str(temp_max), str(temp_min)))
    except:
        funcs.speak("Город не найден!")