import time
import funcs

def time_r():
    try:
        list_of_time = funcs.voice.split()
        if len(list_of_time) == 4:
            if "час" in list_of_time[-1]:
                timer_hour = int(list_of_time[-2])
                timer_min, timer_sec = 0,0
            elif "мин" in list_of_time[-1]:
                timer_hour,timer_sec = 0,0
                timer_min = int(list_of_time[-2])
            elif "сек" in list_of_time[-1]:
                timer_hour,timer_min = 0,0
                timer_sec = int(list_of_time[-2])
        elif len(list_of_time) >= 6:
            if "мин" in list_of_time[-1]:
                timer_hour,timer_sec = 0,0
                timer_min = int(list_of_time[-2])
            elif "сек" in list_of_time[-1]:
                timer_sec = int(list_of_time[-2])
                if "мин" in list_of_time[-3]:
                    timer_min = int(list_of_time[-4])
                    timer_hour = 0
                else:
                    timer_hour = int(list_of_time[-4])
                    timer_min = 0

        timer = timer_hour*3600 + timer_min*60 + timer_sec

        while  timer != 0:
            time.sleep(1)
            print(timer//3600,(timer//60)%60, timer%60, sep=':')
            timer -= 1
        else:
            funcs.speak("Завершено!")

    except:
        funcs.speak("Скажите, например: таймер на 10 секунд")