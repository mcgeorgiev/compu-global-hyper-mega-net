import requests
import json

def getRatingOfFilm (mTitle):
    try:
        ps = {'t': mTitle, 'r': "json", 'tomatoes' : True}
        r = requests.get('http://www.omdbapi.com/?',params = ps)
        result = json.loads(r.text)
        rating = result ["tomatoMeter"]
        return int (rating)
    except:
        return "unknown"

#print getRatingOfFilm ("Inception")
