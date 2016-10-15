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


tempVar = "Test" # Hack around for findByVal

def findall(v, k, apList): #If I find a key, I'll return the value of the key
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
            
def findByVal(val,k): #If I find actor's name, I'll return actor's ID. Can be generalized by introducing a new parameter thingToLookUp instead of hardcoded "id"
    global tempVar #Hack around, can be done recursively
    if type(val) == type({}):
        for k1 in val: #for each key in the dictionary
            #print k1, "\n" #debug
            if val[k1] == k: #if I find the name
                for k2 in val: #Find the ID
                    if k2 == 'id':
                        print val[k2], "VALUE WE WANT"
                        tempVar = val[k2]
            findByVal(val[k1], k)
    elif type(val) == type([]):
        for i,k1 in enumerate(val): # for value in list 
            if k1 == k: #if value equals what we're looking for
                print val[i], "TESTTSTE"
            findByVal(val[i], k)


def pullMoviesFromActor(aName): ##Goes through 3 recursive functions 
    aPlusName = aName.replace(" ","+")
    ps = {'q':aPlusName}
    r = requests.get('http://imdb.wemakesites.net/api/search',params = ps)
    pj = json.loads(r.text)
    print r.url
    names = []
    findall(pj,"names",names) #find all name dicts (only 1)
    findByVal(names,aName) # Find id of actor
    r2 = requests.get('http://imdb.wemakesites.net/api/' + tempVar)
    actorPage = json.loads(r2.text)
    movies = []
    findall(actorPage,"title",movies) #Find all movies the actor is in
    print movies[1:] #movie 0 is actor name lol
    
    
pullMoviesFromActor("Nicolas Cage")


