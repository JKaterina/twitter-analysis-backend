from config import DBConfig, TwitterConfig
from models import col_names
from initialize import *
import json
from sqlalchemy import create_engine
import pandas as pd
import sqlite3

ENTERPRISE_ACCESS = False

def run():
    api = authenticate()
    if api: print("Authentication succesful")
    tweets = extract_tweet_data(api, TwitterConfig.TWITTER_HANDLE, 0)
    tweets_list_of_dicts = []
    for tweet in tweets:
        tweets_list_of_dicts.append(tweet._json)
    if ENTERPRISE_ACCESS:
        list_of_ids = [tweet['id_str'] for tweet in tweets_list_of_dicts] #get list of ids from json
        engagement_metrics_by_id = get_engagement_metrics(list_of_ids)
    else:
        engagement_metrics_by_id = []
    if tweets: print("Tweets extracted")
    with open('raw_data/tweets.json', 'w') as file:
        json_string = json.dumps(tweets_list_of_dicts, indent=4)
        file.write(json_string)  
        data = json.loads(json_string)
        csv_path = process_tweet_data(data, engagement_metrics_by_id)
        print("Tweets processed")

    #Store historic tweets to SQL database
    #Create the database
    print("Creating database...", end = '')
    con = sqlite3.connect("data/twitter_data.sqlite")
    print("Done!")
    with open(csv_path, 'r') as file:
        data_df = pd.read_csv(file)
    print("Loading historic tweets into database...", end = '')
    data_df.to_sql('tweets', con=con, index=False, index_label='tweet_id', if_exists='replace')
    print("Done!")

if __name__ == '__main__':
    run()