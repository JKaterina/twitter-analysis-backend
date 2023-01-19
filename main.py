import tweepy
import pandas as pd
from decouple import config

consumer_key = config('consumer_key')
consumer_secret = config('consumer_secret')
access_token = config('access_token')
access_token_secret = config('access_token_secret')

def authenticate():
    # authorize
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return True

if __name__ == "__main__":
    authenticated = authenticate()
    if authenticated: print("Authentication succesful")
    

    