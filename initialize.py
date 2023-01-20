import tweepy
import pandas as pd
import json
from datetime import datetime
import time
from config import TwitterConfig
from models import col_names

engagement_post_body = {
    "tweet_ids": [],
      "engagement_types": [
        "impressions",
        "engagements",
        "favorites",
        "quote_tweets"
    ],
    "groupings": {
      "grouping name": {
        "group_by": [
          "tweet.id",
          "engagement.type"
        ]
      }
    }
  }

def authenticate():
    # authorize
    auth = tweepy.OAuthHandler(TwitterConfig.CONSUMER_KEY, TwitterConfig.CONSUMER_SECRET)
    auth.set_access_token(TwitterConfig.ACCESS_TOKEN, TwitterConfig.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api

def extract_tweet_data(api, twitter_handle, timeframe):
    tweets = api.user_timeline(screen_name=twitter_handle, 
                           count=2,
                           include_rts = True,
                           tweet_mode = 'extended')
    #To do: implement engagement api to extract quote tweets, replies, video views, url link clicks, user profile clicks, engagements, impressions
    return tweets

def get_engagement_metrics(list_of_ids):
    # Getting the data using enterprise api
    metrics_by_ids = []
    return metrics_by_ids

def process_tweet_data(tweets_json):
    #To add: quote tweets, replies, video views, url link clicks, user profile clicks, engagements, impressions
    timestamp = datetime.now()
    unix_timestamp = time.mktime(timestamp.timetuple())
    outtweets = [[tweet["id_str"],
              datetime.strftime(datetime.strptime(tweet["created_at"],'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S'),
              tweet["retweet_count"],
              tweet["favorite_count"]] 
             for idx, tweet in enumerate(tweets_json)]
    df = pd.DataFrame(outtweets,columns=["tweet_id","created_at","likes","retweets"])
    path = 'processed_data/{}_tweets_{}.csv '.format(TwitterConfig.TWITTER_HANDLE,unix_timestamp)
    df = df.reindex(columns=col_names, fill_value=0)
    df.to_csv(path,index=False)
    return path

if __name__ == "__main__":
    api = authenticate()
    if api: print("Authentication succesful")
    tweets = extract_tweet_data(api, TwitterConfig.TWITTER_HANDLE, 0)
    if TwitterConfig.ENTERPRISE_BEARER_TOKEN:
        list_of_ids = []
        metrics_by_ids = get_engagement_metrics(list_of_ids)
        # add metrics to tweets json objects
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

        #Store to SQL database

        #Method for periodically adding new tweets
        

    


    