import requests
import json

## OMDB API
ps = {'t': "Groundhog Day", 'r': "json", 'plot': "short"} #Parameters
r = requests.get('http://www.omdbapi.com/?',params = ps)

#print r.url
#print r.text

ps2 = {'q':"Nicolas Cage"}
r2 = requests.get('http://imdb.wemakesites.net/api/search',params = ps2)
          
#print r2.url
#print r2.text

#this function should return a list of name values, copied from SO
def fun(d):
    if 'names' in d:
        yield d['names']
    for k in d:
        if isinstance(d[k], list):
            for i in d[k]:
                for j in fun(i):
                    yield j
                    
def pullMoviesFromActor(aName):
    aName = aName.replace(" ","+")
    ps = {'q':aName}
    r = requests.get('http://imdb.wemakesites.net/api/search',params = ps)
    pj = json.loads(r.text)
    #get names
    #get top name id
    print r.url
    print pj #the whole sjon
    #print list(fun(pj))

    
pullMoviesFromActor("Nicolas Cage")




