import requests
import json


#### OMDB API
##ps = {'t': "Groundhog Day", 'r': "json", 'plot': "short"} #Parameters
##r = requests.get('http://www.omdbapi.com/?',params = ps)
##
###print r.url
###print r.text
##
##ps2 = {'q':"Nicolas Cage"}
##r2 = requests.get('http://imdb.wemakesites.net/api/search',params = ps2)
##
###print r2.url
###print r2.text

#Generalize FindAll, FindByValue
#Generalize final functions
#Finalize genre getting
#Get a list of every movie

tempVar = [] # Hack around for findByVal

#GENERALIZE THOSE 2, so that they CAN work on different API

def findall(v, k, apList): #If I find a key, I'll return the values of the key into the SPECIFIED LIST
    if type(v) == type({}):
        for k1 in v:
            if k1 == k:
                #print v[k1]
                apList.append(v[k1])
            findall(v[k1], k, apList)
    elif type(v) == type([]):
        for i,k1 in enumerate(v): # for value in list
            if k1 == k: #if value equals what we're looking for
                #print v[i]
                apList.append(v[i])
            findall(v[i], k, apList)

def findMore(v, k, nestList): #NOT WORKING v is json, k is list of things to find, nestList is a nestedList of outputs
    if type(v) == type({}):
        for k1 in v:
            for i,val in enumerate(k):
                if k1 == val:
                    nestList[i].append(v[k1])
                findall(v[k1], k, nestList)
    elif type(v) == type([]):
        for i,k1 in enumerate(v): # for value in list
            for j,val in enumerate(k):
                if k1 == val: #if value equals what we're looking for
                    nestList[j].append(v[i])
                findall(v[i], k, nestList)


def findByVal(val,k, thingToFind): #If I find actor's name, I'll return actor's ID.
    global tempVar #Hack around, can be done recursively
    if type(val) == type({}):
        for k1 in val: #for each key in the dictionary
            #print k1, "\n" #debug
            if val[k1] == k: #if I find the name
                for k2 in val: #Find the ID
                    if k2 == thingToFind:
                        print val[k2], "VALUE WE WANT"
                        tempVar.append(val[k2])
            findByVal(val[k1], k, thingToFind)
    elif type(val) == type([]):
        for i,k1 in enumerate(val): # for value in list
            if k1 == k: #if value equals what we're looking for
                print val[i], "TESTTSTE"
            findByVal(val[i], k, thingToFind)

#can be generalized - need to generalize findall, findByValue first!

def pullGenres(mTitle):
    ps = {'q':mTitle}
    r = requests.get('http://imdb.wemakesites.net/api/search',params = ps)
    pj = json.loads(r.text)
    findByVal(pj,mTitle,'id') # Find id of actor
    r2 = requests.get('http://imdb.wemakesites.net/api/' + tempVar[0])
    movieList = json.loads(r2.text)
    genres = []
    findall(movieList,"genres",genres) #access genres
    print genres
    return genres

def pullActors(mTitle):
    ps = {'q':mTitle}
    r = requests.get('http://imdb.wemakesites.net/api/search',params = ps)
    pj = json.loads(r.text)
    findByVal(pj,mTitle,'id') # Find id of actor
    r2 = requests.get('http://imdb.wemakesites.net/api/' + tempVar[0])
    movieList = json.loads(r2.text)
    actors = []
    findall(movieList,"cast",actors) #access genres
    print actors
    return actors

def pullMoviesFromActor(aName): ##Goes through 3 recursive functions
    aPlusName = aName.replace(" ","+")
    ps = {'q':aPlusName}
    r = requests.get('http://imdb.wemakesites.net/api/search',params = ps)
    pj = json.loads(r.text)
    #print r.url
    names = []
    findall(pj,"names",names) #find all name dicts (only 1)
    findByVal(names,aName,'id') # Find id of actor
    r2 = requests.get('http://imdb.wemakesites.net/api/' + tempVar[0])
    actorPage = json.loads(r2.text)
    movies = []
    findall(actorPage,"title",movies) #Find all movies the actor is in
    print movies[1:] #movie 0 is actor name lol
    return movies[1:]

#NOT WORKING
def pullAandG(mTitle): #Not Working
    ps = {'q':mTitle}
    r = requests.get('http://imdb.wemakesites.net/api/search',params = ps)
    pj = json.loads(r.text)
    findByVal(pj,mTitle,'id') # Find id of actor
    r2 = requests.get('http://imdb.wemakesites.net/api/' + tempVar[0])
    movieList = json.loads(r2.text)
    aAndG = [[],[]]
    findMore(movieList,["cast","genres"],aAndG) #access genres
    print aAndG

pullMoviesFromActor("Nicolas Cage")
#pullAandG("Inception")
#pullGenres("Tangled")
