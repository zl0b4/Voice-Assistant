import requests
import webbrowser
import funcs

def google_find():
    find = funcs.voice.split()[1:]
    def googleSearch(query):
        url = 'https://www.google.com/search?q='
        query = {'q': query}
        urllink = requests.get(url, params=query)
        webbrowser.open(urllink.url)
    googleSearch(" ".join(find))
