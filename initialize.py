import tweepy
import pandas as pd
import json
from datetime import datetime
import time
from config import TwitterConfig
from models import col_names

import gnip_insights_interface.engagement_api as engagement_api

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

#function to authenticate tweepy for API access
def authenticate():
    # authorize
    auth = tweepy.OAuthHandler(TwitterConfig.CONSUMER_KEY, TwitterConfig.CONSUMER_SECRET)
    auth.set_access_token(TwitterConfig.ACCESS_TOKEN, TwitterConfig.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api

#function to extract tweet data using a given authenticated api connection and twitter_handle, returns tweets in json string format
def extract_tweet_data(api, twitter_handle, timeframe):
    tweets = api.user_timeline(screen_name=twitter_handle, 
                           count=200,
                           include_rts = True,
                           tweet_mode = 'extended')
    return tweets

#function to get engagement metric from engagement api using gnip_insights_interface
def get_engagement_metrics(list_of_ids):
    # Getting the data using enterprise api
    engagement_post_body['tweet_ids'] = list_of_ids
    engagement_post_body['engagement_types'] = ['impressions','engagements','favorites','quote_tweets','replies','video_views','url_clicks','user_profile_clicks','engagements']
    #make request
    engagement_api.query_tweets(engagement_post_body['tweet_ids'],['tweet_id','engagement_type'],'totals',engagement_post_body['engagement_types'],25,)
    #return dict by id
    return metrics_by_ids

#function to process json data, extract relevant data and store to csv. returns path to csv
def process_tweet_data(tweets_json, engagement_metrics_by_id={}):
    #To add: quote tweets, replies, video views, url link clicks, user profile clicks, engagements, impressions
    timestamp = datetime.now()
    unix_timestamp = time.mktime(timestamp.timetuple())
    outtweets = [[tweet["id_str"],
              datetime.strftime(datetime.strptime(tweet["created_at"],'%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S'),
              tweet["retweet_count"],
              tweet["favorite_count"],
              tweet['entities']['hashtags']]
             for idx, tweet in enumerate(tweets_json)]
    df = pd.DataFrame(outtweets,columns=["tweet_id","created_at","likes","retweets","hashtags"])
    path = 'processed_data/{}_tweets_{}.csv '.format(TwitterConfig.TWITTER_HANDLE,unix_timestamp)
    df = df.reindex(columns=col_names, fill_value=0)
    if engagement_metrics_by_id:
      #routine to add engagement metrics before csv gets saved
      for id, metrics in engagement_metrics_by_id.items():
        for metric in metrics:
          df[id][metric.key()] = metric.value()
    df.to_csv(path,index=False)
    return path

if __name__ == "__main__":
    api = authenticate()
    if api: print("Authentication succesful")
    tweets = extract_tweet_data(api, TwitterConfig.TWITTER_HANDLE, 0)
    if TwitterConfig.ENTERPRISE_API:
        list_of_ids = [tweet['id_str'] for tweet in tweets] #get list of ids from json
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
        

    


    