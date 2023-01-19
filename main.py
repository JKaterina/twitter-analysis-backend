import tweepy
import pandas as pd
import json
from decouple import config

consumer_key = config('consumer_key')
consumer_secret = config('consumer_secret')
access_token = config('access_token')
access_token_secret = config('access_token_secret')
twitter_handle = config('twitter_handle')

def authenticate():
    # authorize
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def extract_tweet_data(api, twitter_handle, timeframe):
    tweets = api.user_timeline(screen_name=twitter_handle, 
                           count=2,
                           include_rts = True,
                           tweet_mode = 'extended')
    return tweets

if __name__ == "__main__":
    api = authenticate()
    if api: print("Authentication succesful")
    tweets = extract_tweet_data(api, twitter_handle, 0)
    tweets_list_of_dicts = []
    for tweet in tweets:
        tweets_list_of_dicts.append(tweet._json)
    with open('raw_data/tweets.json', 'w') as file:
        file.write(json.dumps(tweets_list_of_dicts, indent=4))

    


    