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
    #To do: implement engagement api to extract quote tweets, replies, video views, url link clicks, user profile clicks, engagements, impressions
    return tweets

def process_tweet_data(tweets_json):
    #To add: quote tweets, replies, video views, url link clicks, user profile clicks, engagements, impressions
    
    outtweets = [[tweet["id_str"],
              tweet["created_at"],
              tweet["retweet_count"],
              tweet["favorite_count"]] 
             for idx, tweet in enumerate(tweets_json)]
    df = pd.DataFrame(outtweets,columns=["id","created_at","retweet_count","favorite_count"])
    df.to_csv('processed_data/%s_tweets.csv' % twitter_handle,index=False)
    return True

if __name__ == "__main__":
    api = authenticate()
    if api: print("Authentication succesful")
    tweets = extract_tweet_data(api, twitter_handle, 0)
    tweets_list_of_dicts = []
    for tweet in tweets:
        tweets_list_of_dicts.append(tweet._json)
    if tweets: print("Tweets extracted")
    with open('raw_data/tweets.json', 'w') as file:
        json_string = json.dumps(tweets_list_of_dicts, indent=4)
        file.write(json_string)  
        data = json.loads(json_string)
        process_tweet_data(data)
        print("Tweets processed")
        

    


    