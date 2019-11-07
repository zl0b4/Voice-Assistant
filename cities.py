import os
import random
import time
import funcs
import pyttsx3
import speech_recognition as sr
def game():
    os.chdir(r'C:\Users\User\Desktop\ \programming\helper_1')
    cities_file = open('cities.txt')
    cities = cities_file.readlines()
    cities_main = []

    print("""Добро пожаловать в игру 'Города'!
    На ответ даётся 15 секунд.
    Называть нужно исключительно существующие города и только на последнюю букву(если это не ь, ъ, ы)
    """)

    funcs.speak("Кто начинает?(Я/Компьютер)")
    for i in cities:
        cities_main.append(i.split('\n')[0])
    cities_clear = cities_main.copy()


    if ans == "Я":
        city = input("Введите город: ").capitalize()
        print()
        if city == "Йошкар-ола":
            city = "Йошкар-Ола"

    elif ans == "Компьютер":
        city_num = random.randint(0,len(cities_clear))
        city = cities_clear[city_num]
        print()
        if city == "Йошкар-ола":
            city = "Йошкар-Ола"

    else:
        print("Введите либо 'Я', либо 'Компьютер'")


    def city_game(city, cities_clear):
        if city[-1] not in ['ь', 'ъ', 'ы','ц']:
            last_letter = city[-1].upper()
            for i in cities_clear:
                if i[0] == last_letter:
                    list.append(i)
            index = random.randint(0,len(list))
            cit = list[index].rstrip()

            print(cit)
            print()
            cities_clear.remove(cit)
            cities_clear.remove(city)
        else:
            last_letter = city[-2].upper()
            for i in cities_clear:
                if i[0] == last_letter:
                    list.append(i)
            index = random.randint(0,len(list))
            cit = list[index].rstrip()

            print(cit)
            print()
            cities_clear.remove(cit)
            cities_clear.remove(city)
        last_cit = cit[-1].upper()
        if last_cit in ['Ь', 'Ъ', 'Ы', 'Ц']:
            last_cit = cit[-2].upper()

        return last_cit


    if city in cities_clear:
        list = []
        last_cit = city_game(city, cities_clear)
    else:
       print("Город либо не существует, либо уже был введён")

    while True:
        start = time.time()

        city = input("Введите город: ").capitalize()
        print()
        if city == "Йошкар-ола":
            city = "Йошкар-Ола"

        if city[0] == last_cit:
            if city in cities_clear:
                list = []
                last_cit = city_game(city, cities_clear)

            else:
                print("Город либо не существует, либо уже был введён")
        else:
            print("Введите город на последнюю букву")

        if time.time() - start >= 15:
            print('Вы не успели')
            break


