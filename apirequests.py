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

def findMore(v, k, nestList): #Generalized findall
    if type(v) == type({}):
        for k1 in v: # once for every list in the element K why?
            for i,val in enumerate(k):
                if k1 == val:
                    if v[k1] not in nestList[i]: #Workaround, f it
                        nestList[i].append(v[k1])
                findMore(v[k1], k, nestList)
    elif type(v) == type([]):
        for i,k1 in enumerate(v): # for value in list
            for j,val in enumerate(k):
                if k1 == val: #if value equals what we're looking for
                    nestList[j].append(v[i])
                findMore(v[i], k, nestList)


def findByVal(val,k, thingToFind): #If I find actor's name, I'll return actor's ID.
    # global tempVar
    print tempVar
    #Hack around, can be done recursively
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

def pullThings(mTitle,things,wantRating): #HAS TO BE SPECIFIC THINGS FROM THE API, BUT IT'S WORKING YAY
    #Returns a list of lists, where the categories are in order they were put in
    thingList = [[] for i in range(len(things))]
    if(wantRating):
        ps1 = ps = {'t': mTitle, 'r': "json", 'plot': "short", 'tomatoes' : True}
        r1 = requests.get('http://www.omdbapi.com/?',params = ps1)
        ratingJson = json.loads(r1.text)
        mRating = ratingJson ["tomatoMeter"] #Rating of the movie
        thingList.append(mRating)
    ##API 2
    ps = {'q':mTitle}
    r = requests.get('http://imdb.wemakesites.net/api/search',params = ps)
    pj = json.loads(r.text)
    findByVal(pj,mTitle,'id') # Find id of actor
    r2 = requests.get('http://imdb.wemakesites.net/api/' + tempVar[0])
    movieList = json.loads(r2.text)
    findMore(movieList,things,thingList) #access genres
    print thingList


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


pullActors("Blair Witch")
#pullMoviesFromActor("Nicolas Cage")
#pullAandG("Inception")
#pullGenres("Tangled")

#pullThings("Inception",["cast","released"],1)
