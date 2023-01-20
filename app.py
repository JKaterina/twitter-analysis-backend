import sqlite3
import streamlit as st
import pandas as pd
import numpy as np
from config import DBConfig
import datetime

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
    return df, timestamp

# Graph models
@st.cache(show_spinner=False)
def likes_per_tweet(df):
    return df['Likes']

# App settings
st.set_page_config(layout="wide", page_title='Tweets Dashboard')

data, timestamp = get_data_from_sql()

plot_freq_options = {
    'Hourly': 'H',
    'Four Hourly': '4H',
    'Daily': 'D'
}

# Sidebar settings

# date_options = data.Timestamp.dt.date.unique()
# start_date_option = st.sidebar.selectbox('Select Start Date', date_options, index=0)
# end_date_option = st.sidebar.selectbox('Select End Date', date_options, index=len(date_options)-1)

# Adding content and graphs

st.write('Total tweet count: {}'.format(data.shape[0]))
st.write('Data last loaded {}'.format(timestamp))

col1, col2, col3 = st.beta_columns(3)

col1.subheader('Likes per Tweet')
plotdata = likes_per_tweet(data)
col1.line_chart(plotdata)
