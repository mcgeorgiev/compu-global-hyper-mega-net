import urllib2
import json
import random
import requests
from datetime import datetime
random.seed(datetime.now())


API_BASE="http://bartjsonapi.elasticbeanstalk.com/api"

followQuestions = [" is in this movie, are you a fan of theirs?",
                    [" also starred in "," have you seen that movie?"]]
tempVar = []

def lambda_handler(event, context):

    if event["session"]["new"]:
        event['session'] = on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])

def on_session_started(session_started_request, session):
    print "Starting new session."
    print session
    session['attributes']['movie'] = []
    return session

def on_launch(launch_request, session):
    return get_welcome_response()

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]
    #session['attributes']['x'] = session['attributes'].get('x', 0) + 1
    # session_numbers = session['attributes'].keys()
    print '********'
    print session['attributes']
    #session['attributes']['movie'].append(intent_request["intent"]["slots"]["movies"]["value"])
    print session
    if intent_name == "GetMovie":
        return get_movie(session['attributes'], intent_request["intent"]["slots"]["movies"]["value"])
    elif intent_name == "No":
        return no(session['attributes'])
    elif intent_name == "Yes":
        return yes(session['attributes'])
    elif intent_name == "GetActor":
        return get_actor()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    print "Ending session."
    # Cleanup goes here...

def handle_session_end_request():
    card_title = "Movies - Thanks"
    speech_output = "Thank you for using the Movies skill.  See you next time!"
    should_end_session = True

    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))

def get_welcome_response():
    session_attributes = {}
    card_title = "Welcome Response"
    speech_output = "Welcome to Alexa movie database. " \
                    "You can ask me for movies, or " \
                    "actors."
    reprompt_text = "Please ask me about the movie The Simpsons Movie."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_movie(session, movieName):
    session_attributes = session
    card_title = "Movie search"
    reprompt_text = ""
    should_end_session = False
    speech_output = "You searched for %s" %(movieName)

    text = followQuestions[1]


    # filmId = findFilmId(movieName)
    # print filmId
    # temp = findFilmGenreAndCast(filmId)
    # actor = random.choice([1])
    actor = random.choice(findFilmGenreAndCast(findFilmId(movieName)))
    print actor
   #actor = random.choice(temp[1])
    movie = random.choice(findActorFilms(findActorId(actor)))

    print actor


    movie = random.choice(findActorFilms(findActorId(actor)))
    textfinal = actor + text[0] + movie + text[1]

    speech_output+= ', '
    speech_output += textfinal
    session['movie'].append(movieName)
    dicti = {"question":speech_output, "actor" : actor, "film" : movie}
    session['movie'].append(dicti)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_actor(session, actorName):
    session_attributes = session
    card_title = "Actor search"
    reprompt_text = ""
    should_end_session = False
    speech_output = "You searched for %s" %(actorName)

    text = random.choice(followQuestions)
    place = followQuestions.index(text)

    if place == 0:
        text.format(actorName)
    elif place == 1:

        text.format("actor name", "movie 2")

    speech_output+= ', '
    speech_output += text
    session['movie'].append(actorName)
    dicti = {"question":text, "actor" : "actor name", "film" : "movie 2"}
    session['movie'].append(dicti)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



def yes(attributes):
    card_title = "they answered yes"
    reprompt_text = ''
    should_end_session = False
    text = followQuestions[1]#random.choice(followQuestions)
    #num = followQuestions.count('{')

    data = attributes['movie'][-1]

    print data['film']
    actor = random.choice(findFilmGenreAndCast(findFilmId(data['film'])))
    print actor
    movie = random.choice(findActorFilms(findActorId(actor)))


    attributes['movie'].append({"question":text, "actor" : actor, "film" : movie})

    rating = getRatingOfFilm(movie)
    if rating <10:
        info = "I think the film is pretty shite"
    elif rating >10 and rating < 20:
        info = "I think the film is quite bad"
    elif rating >20 and rating < 30:
        info = "I think the film is probably so bad its good"
    elif rating >30 and rating < 60:
        info = "I think the film is bad to reasonable"
    elif rating > 60 and rating < 70:
        info = "I think the film is actually alright"
    elif rating > 70 and rating < 80:
        info = "I think the film is very good"
    elif rating > 80 and rating < 100:
        info = "I think the film is really very good"
    else:
        info = 'Im not sure about the film'

    textfinal = actor + text[0] + movie +', ' +info +', '+ text[1]
    speech_output = ''
    speech_output += textfinal
    attributes['movie'].append(movie)
    dicti = {"question":speech_output, "actor" : actor, "film" : movie}
    attributes['movie'].append(dicti)

    return build_response(attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def no(attributes):
    card_title = "they answered no"
    reprompt_text = ''
    should_end_session = False
    text = followQuestions[1]#random.choice(followQuestions)
    #num = followQuestions.count('{')

    data = attributes['movie'][-1]

    actor = random.choice(findFilmGenreAndCast(findFilmId(data['film'])))
    movie = random.choice(findActorFilms(findActorId(actor)))
    #text.format(actor, film)

    attributes['movie'].append({"question":text, "actor" : actor, "film" : movie})

    #attributes['movie'].append(movie)

    rating = getRatingOfFilm(movie)
    if rating <10:
        info = "I think the film is pretty shite"
    elif rating >10 and rating < 20:
        info = "I think the film is quite bad"
    elif rating >20 and rating < 30:
        info = "I think the film is probably so bad its good"
    elif rating >30 and rating < 60:
        info = "I think the film is bad to reasonable"
    elif rating > 60 and rating < 70:
        info = "I think the film is actually alright"
    elif rating > 70 and rating < 80:
        info = "I think the film is very good"
    elif rating > 80 and rating < 100:
        info = "I think the film is really very good"
    else:
        info = 'Im not sure about the film'

    textfinal = actor + text[0] + movie +', ' +info +', '+ text[1]
    speech_output = ''
    speech_output += textfinal
    dicti = {"question":speech_output, "actor" : actor, "film" : movie}
    attributes['movie'].append(dicti)
    return build_response(attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    # text = random.choice(followQuestions)
    # place = followQuestions.index(text)

    # if place == 0:
    #     text.format("actor name")
    # elif place == 1:
    #     text.format("actor name", "movie 2")


    # attributes['movie'].append({"question":text, "actor" : "actor name", "film" : "movie 2"})

    # return build_response(attributes, build_speechlet_response(
    #     card_title, text, reprompt_text, should_end_session))


def makeActorList(mTitle):
    ps = {'t': mTitle, 'r': "json", 'tomatoes' : True}
    r = requests.get('http://www.omdbapi.com/?',params = ps,timeout=10)
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

def findSome(v, k, apList, instances):
    if len(apList) >= instances+1:
        return None
    elif type(v) == type({}):
        for k1 in v:
            if k1 == k:
                #print v[k1]
                apList.append(v[k1])
            findSome(v[k1], k, apList, instances)
    elif type(v) == type([]):
        for i,k1 in enumerate(v): # for value in list
            if k1 == k: #if value equals what we're looking for
                #print v[i]
                apList.append(v[i])
            findSome(v[i], k, apList, instances)

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
    global tempVar
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

def findByVal2(val,k, thingToFind, testList): #If I find actor's name, I'll return actor's ID.
    #Hack around, can be done recursively
    if type(val) == type({}):
        for k1 in val: #for each key in the dictionary
            if val[k1] == k:
                for k2 in val:
                    if k2 == thingToFind:
                        print val[k2]
                        testList.append(val[k2])
                    findByVal2(val[k1],k, thingToFind, testList)
    elif type(val) == type([]):
        for i in val:
            findByVal2(i,k,thingToFind,testList)

def pullGenres(mTitle):
    ps = {'q':mTitle}
    r = requests.get('http://imdb.wemakesites.net/api/search',params = ps, timeout = 10)
    pj = json.loads(r.text)
    tempList = []
    #print pj
    findByVal2(pj,mTitle,'id',tempList) # Find id of s
    if len(tempList)>0:
        r2 = requests.get('http://imdb.wemakesites.net/api/' + tempList[0], timeout = 10)
        movieList = json.loads(r2.text)
        genres = []
        findall(movieList,"genres",genres) #access genres
        print genres
        return genres
    else:
        print -1
        return 1






def pullThings(mTitle,things,wantRating): #HAS TO BE SPECIFIC THINGS FROM THE API, BUT IT'S WORKING YAY
    #Returns a list of lists, where the categories are in order they were put in
    thingList = [[] for i in range(len(things))]
    if(wantRating):
        ps1 = ps = {'t': mTitle, 'r': "json", 'plot': "short", 'tomatoes' : True}
        r1 = requests.get('http://www.omdbapi.com/?',params = ps1, timeout = 10)
        ratingJson = json.loads(r1.text)
        mRating = ratingJson ["tomatoMeter"] #Rating of the movie
        thingList.append(mRating)
    ##API 2
    ps = {'q':mTitle}
    r = requests.get('http://imdb.wemakesites.net/api/search',params = ps, timeout = 10)
    pj = json.loads(r.text)
    findByVal(pj,mTitle,'id') # Find id of actor
    r2 = requests.get('http://imdb.wemakesites.net/api/' + tempVar[0], timeout = 10)
    movieList = json.loads(r2.text)
    findMore(movieList,things,thingList) #access genres
    print thingList


#can be generalized - need to generalize findall, findByValue first!


def pullActors(mTitle):
    ps = {'q':mTitle}
    r = requests.get('http://imdb.wemakesites.net/api/search',params = ps, timeout = 10)
    pj = json.loads(r.text)
    findByVal(pj,mTitle,'id') # Find id of actor
    r2 = requests.get('http://imdb.wemakesites.net/api/' + tempVar[0], timeout = 10)
    movieList = json.loads(r2.text)
    actors = []
    findall(movieList,"cast",actors) #access genres
    print actors
    return actors[:3]

def pullMoviesFromActor(aName): ##Goes through 3 recursive functions
    aPlusName = aName.replace(" ","+")
    ps = {'q':aPlusName}
    r = requests.get('http://imdb.wemakesites.net/api/search',params = ps, timeout = 10)
    pj = json.loads(r.text)
    #print r.url
    names = []
    findall(pj,"names",names) #find all name dicts (only 1)
    findByVal(names,aName,'id') # Find id of actor
    r2 = requests.get('http://imdb.wemakesites.net/api/' + tempVar[0], timeout = 10)
    actorPage = json.loads(r2.text)
    movies = []
    findSome(actorPage,"title",movies,5) #Find all movies the actor is in
    print movies[1:] #movie 0 is actor name lol
    return movies[1:]

tempVar = [] # Hack around for findByVal

def getRatingOfFilm (mTitle):
    try:
        ps = {'t': mTitle, 'r': "json", 'tomatoes' : True}
        r = requests.get('http://www.omdbapi.com/?',params = ps)
        result = json.loads(r.text)
        rating = result ["tomatoMeter"]
        return int (rating)
    except:
        return "unknown"


# get the Id of an actor based on their full name
def findActorId (actorName):
    ps = {'q': actorName}
    r = requests.get('http://imdb.wemakesites.net/api/search',params = ps)
    result = json.loads(r.text)
    people = result ["data"] ["results"] ["names"]

    for person in people:
        if person ["title"].lower() == actorName.lower():
            print str(person ["id"])
            return str(person ["id"]) # type str
    return 'nm0000102'


# get the actor's film
def findActorFilms (actorId):
    r = requests.get('http://imdb.wemakesites.net/api/' + actorId)
    result = json.loads (r.text)
    films = result ["data"] ["filmography"]
    theirFilms = []

    for film in films:
        theirFilms += [film ["title"]]

    return theirFilms # type list

# get the Id of a film based on its title
def findFilmId (filmTitle):
    ps = {'q': filmTitle}
    r = requests.get('http://imdb.wemakesites.net/api/search',params = ps)
    result = json.loads (r.text)

    films = result ["data"] ["results"] ["titles"]
    for film in films:
        if (film ["title"]).lower() == filmTitle.lower():
            return str(film["id"]) # type str
    return 'tt0087277'

# get the genre and cast of a film based on its Id
def findFilmGenreAndCast (filmId):
    r = requests.get('http://imdb.wemakesites.net/api/' + filmId)
    result = json.loads (r.text)
    genres = result ["data"] ["genres"]
    cast = result ["data"] ["cast"]
    # tuple of ( list of genres, list of cast)
    return cast

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }
