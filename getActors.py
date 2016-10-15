import requests
import json

def makeActorList (mTitle):
    ps = {'t': mTitle, 'r': "json", 'tomatoes' : True}
    r = requests.get('http://www.omdbapi.com/?',params = ps)
    result = json.loads(r.text)
    
    actList = []
    actors = str((result ["Actors"]))
    actList = actors.split (",")
    i = 0
    for actor in actList:
        if actor [0] == " ":
            actList [i]  = actor [1:]
        i += 1
    return actList

print makeActorList ("Inception")
