import ast
import json
import sqlite3
import streamlit as st
import pandas as pd
import numpy as np
from config import DBConfig
import datetime
from collections import Counter

@st.cache(allow_output_mutation=True, show_spinner=False)
def get_connection():
    return sqlite3.connect("data/twitter_data.sqlite", check_same_thread=False)

@st.cache(allow_output_mutation=True, show_spinner=True, ttl=6*60)
def get_data_from_sql():
    timestamp = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    df = pd.read_sql_query("SELECT * from tweets", get_connection())
    df = df.rename(columns={'tweet_id': 'Tweet', 'created_at': 'Timestamp',
                            'likes': 'Likes', 'impressions': 'Impressions',
                            'engagement_rate': 'Engagement Rate', 'retweets': 'Retweets',
                            'quote_tweets': 'Quote Tweets', 'replies': 'Replies',
                            'link_clicks': 'Link Clicks', 'video_views': 'Video Views',
                            'profile_clicks': 'Profile Clicks', 'hashtags': 'Hashtags',
                            'pc_likes' : 'Change in Likes', 'pc_impressions':'Change in Impressions',
                            'pc_engagement_rate': 'Change in Engagement Rate' })
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df.sort_values(by='Timestamp')
    return df, timestamp

@st.cache(show_spinner=False)
def filter_by_date(df, start_date, end_date):
    df_filtered = df.loc[(df.Timestamp.dt.date >= start_date) & (df.Timestamp.dt.date <= end_date)]
    return df_filtered

# Graph models
@st.cache(show_spinner=False)
def likes_per_tweet(df):
    return df['Likes']

@st.cache(show_spinner=False)
def retweets_per_tweet(df):
    return df['Retweets']

@st.cache(show_spinner=False)
def top_hashtags(df,n):
    hashtags = [[hashtag['text'] for hashtag in ast.literal_eval(tweet)] for tweet in df['Hashtags'].values]
    counts = Counter(list(np.concatenate(hashtags).flat)).most_common(n)
    return counts

# App settings
st.set_page_config(layout="wide", page_title='Tweets Dashboard')

data, timestamp = get_data_from_sql()

plot_freq_options = {
    'Hourly': 'H',
    'Four Hourly': '4H',
    'Daily': 'D'
}

# Sidebar settings
date_options = data.Timestamp.dt.date.unique()
start_date_option = st.sidebar.selectbox('Select Start Date', date_options, index=0)
end_date_option = st.sidebar.selectbox('Select End Date', date_options, index=len(date_options)-1)

# Adding content and graphs

st.write('Total tweet count: {}'.format(data.shape[0]))
st.write('Data last loaded {}'.format(timestamp))
st.write('Top Hashtags: {}'.format(top_hashtags(data,5)))
col1, col2, col3 = st.columns(3)

col1.subheader('Likes per Tweet')
plotdata = likes_per_tweet(data)
col1.line_chart(plotdata)

col2.subheader('Retweets per Tweet')
plotdata = retweets_per_tweet(data)
col2.line_chart(plotdata)
