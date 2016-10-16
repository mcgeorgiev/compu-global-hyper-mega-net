import tweepy
import time

consumer_key =  '5lXCt4itbUjwYyPN9gCA49fDi'
consumer_secret =  'enKbKTUHwBTfULwgTw9PrPsZ0OMjex7dOYBHHLro3xD4m1o5hs'
access_token = '449672816-sLXWbt5QKjyfRnTPHiJb18keCHAK7mTIpDGcXggB'
access_token_secret = 'W0o3e3nMytXZLUMfjSVXc6DNgXGGGkpUprv3HhHfOY2Ba'
starttime = time.time()


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
data = api.rate_limit_status()
print data['resources']['statuses']
print data['resources']['users']

search_text = '"what is up"'
search_result = api.search(search_text, lang='en')
for i in search_result:
    #print i.text
    try:
        id = i.entities['user_mentions'][0]['id']
        tweet = api.get_status(id)
        print '******'
        if '//' in tweet.text or 'www' in tweet.text:# or tweet['lang'] is not 'en':
            continue
        else:
            tweet_words = tweet.text
            print tweet_words
            #x = tweet_words.index('@')
            #y = tweet_words[x:].index(' ')
            #print tweet_words[:x] + tweet_words[:y]
            print '________'
            break
    except:
        continue
# count = 0
# for i in tweepy.Cursor(api.search, q=search_text, result_type='recent', count=200, lang='en').items():
#     count +=1
#     if count == 50:
#         break
#
#     try:
#         id = i.entities['user_mentions'][0]['id']
#     except:
#         continue
#     tweet = api.get_status(id)
#     print '******'
#     if '//' in tweet.text or 'www' in tweet.text or tweet.lang is not 'en':
#         continue
#     else:
#         tweet_words = tweet.text
#         print tweet_words
#         #x = tweet_words.index('@')
#         #y = tweet_words[x:].index(' ')
#         #print tweet_words[:x] + tweet_words[:y]
#         print '________'
#         break
    #except:
    #    print 'broken'
    #    continue




print time.time()-starttime
