import urllib2
import json
import random
import requests

API_BASE="http://bartjsonapi.elasticbeanstalk.com/api"

followQuestions = ["{0} is in this movie, are you a fan of theirs?",
                    "{0} also starred in {1}, have you seen that movie?"]

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

    text = followQuestions[1]# random.choice(followQuestions)
    #place = followQuestions.index(text)

    num = text.count("{")

    if num == 1:
        text.format(random.choice(pullActors(movieName)))
    elif num == 2:
        actor = random.choice(pullActors(movieName))
        movie = random.choice(pullMoviesFromActor(actor))
        text.format(actor, movie)

    speech_output+= ', '
    speech_output += text
    session['movie'].append(movieName)
    dicti = {"question":text, "actor" : actor, "film" : movie}
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

    data = attributes['movies'][-1]

    # if num == 0:
    #     data
    #     text.format("actor name")
    # elif num == 1:
    #     text.format("actor name", "movie 2")
    actor = pullActors(data['movie'])
    film = pullMoviesFromActor(actor)
    text.format(actor, film)

    attributes['movie'].append({"question":text, "actor" : actor, "film" : film})

    return build_response(attributes, build_speechlet_response(
        card_title, text, reprompt_text, should_end_session))


def no(attributes):
    card_title = "they answered no"
    reprompt_text = ''
    should_end_session = False
    text = random.choice(followQuestions)
    place = followQuestions.index(text)

    if place == 0:
        text.format("actor name")
    elif place == 1:
        text.format("actor name", "movie 2")


    attributes['movie'].append({"question":text, "actor" : "actor name", "film" : "movie 2"})

    return build_response(attributes, build_speechlet_response(
        card_title, text, reprompt_text, should_end_session))

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
