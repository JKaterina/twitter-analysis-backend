import os

from decouple import config

class TwitterConfig:
    CONSUMER_KEY = config('CONSUMER_KEY')
    CONSUMER_SECRET = config('CONSUMER_SECRET')
    ACCESS_TOKEN = config('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = config('ACCESS_TOKEN_SECRET')
    TWITTER_HANDLE = config('TWITTER_HANDLE')
    # this token comes from the registration with Twitter Engagement API
    ENTERPRISE_BEARER_TOKEN = config('ENTERPRISE_BEARER_TOKEN')

class DBConfig:
    DB_USER = config('DB_USER')
    DB_PWORD = config('DB_PWORD')
    DB_HOST = config('DB_HOST')