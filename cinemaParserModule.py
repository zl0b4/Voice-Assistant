import datetime
import requests
import json
import funcs
from bs4 import BeautifulSoup

class Parser:
    def __init__(self, url):
        self.header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"}
        self.session = requests.Session()
        self.session.header = self.header
        self.html = self.session.post(url).text
        self.soup = BeautifulSoup(self.html, "html.parser")
        if "sky-cinema" in url:
            self.cinema = "SC"
        else:
            self.cinema = "CK"

    def getFilmsParameters(self):
        try:
            films = {}
            filmsParas = ""
            section = self.soup.find("div",{"class":"afisha-view afisha-view-list show"})
            film_det = section.find_all("div", {"class":"film-detail"})
            for elem in film_det:
                for elem2 in elem.find_all("div", {"class":"film-seances filter-block"}):
                    for elem3 in elem2:
                        if (elem3.find("a") != None) and (elem3.find("a") != -1):
                            currFilmParas = elem3.find("a").get("onclick").replace("prebookManager.showHall(","").replace(")", "").replace(";","").split()[0]
                            if currFilmParas != "return":
                                filmsParas += currFilmParas.replace("}", ",")+f"\"time\":'{elem3.find('a').get_text()}', \"cost\":'{elem3.find('span').get_text()+' руб'}', \"format\":'{elem3.find('li').get('data-title')}', "+"}, "
                films[elem.find("h3", {"class": "film-title"}).get_text()] = elem.find("p", {"class":"film-genre"}).get_text(), eval(filmsParas), elem.find("h3", {"class": "film-title"}).find("a").get("href")
            return films
        except:
            return True

def cinemaParser(cmdType):
    cmd = funcs.voice

    if "континент" in cmd.lower():
        url = "https://conti.sky-cinema.ru/"

    elif "современник" in cmd.lower():
        url = "https://sovr.sky-cinema.ru/"

    else:
        url = "http://gd.sky-cinema.ru/"

    Helper = Parser(url)

    if cmdType == "findFilms":
        films = Helper.getFilmsParameters()
        try:
            if films:
                if datetime.datetime.now().hour != 0:
                    funcs.speak("На сегодня нет свободных сеансов, посмотрим на завтра")
                    url += "?schedule_date=2019-{}-{}&schedule_list_ajax=Y".format(datetime.datetime.now().day+1, datetime.datetime.now().month)
                else:
                    url += "?schedule_date=2019-{}-{}&schedule_list_ajax=Y".format(datetime.datetime.now().day, datetime.datetime.now().month)
                Helper = Parser(url)
                films = Helper.getFilmsParameters()

            for elem in films:
                funcs.speak(elem)
            funcs.speak("Если вы хотите посмотреть информацию о фильме, укажите его название в конце предложения, в именительном падеже. Также вы можете указать любой филиал skycinema перед названием фильма, по умолчанию я буду искать фильмы в Гостинном дворе.")
        except:
            funcs.speak("К сожалению, я не могу найти фильмы в данном филиале")
        
    if cmdType == "findFilmInfoInCinema":
        try:
            films = Helper.getFilmsParameters()
            if films:
                if datetime.datetime.now().hour != 0:
                    funcs.speak("На сегодня нет свободных сеансов, посмотрим на завтра")
                    url += "?schedule_date=2019-{}-{}&schedule_list_ajax=Y".format(datetime.datetime.now().day+1, datetime.datetime.now().month)
                else:
                    url += "?schedule_date=2019-{}-{}&schedule_list_ajax=Y".format(datetime.datetime.now().day, datetime.datetime.now().month)
                Helper = Parser(url)
                films = Helper.getFilmsParameters()

            filmName = cmd.split()[-1].title()
            if filmName in films:
                funcs.speak("Вот что мне удалось найти")
                funcs.speak(films[filmName][0])
                for i in range(len(films[filmName][1])):
                    print(f'\n\nНачало в: {films[filmName][1][i]["time"]}\nСтоимость: {films[filmName][1][i]["cost"]}\nФормат: {films[filmName][1][i]["format"]}')
            else:
                funcs.speak("Данного фильма нет в прокате")
        except:
            funcs.speak("К сожалению, я не могу найти фильм в данном филиале")