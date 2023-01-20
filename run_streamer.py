import os, logging, datetime
from logging.handlers import RotatingFileHandler
import sqlite3
from config import TwitterConfig
from stream_tweets import TweetListener
from tweepy import Stream
from tweepy import OAuthHandler

log_dir = 'Logs'
if not os.path.exists(log_dir):
    os.mkdir(log_dir)
log_name = 'streaming_{}.log'.format(datetime.date.today().strftime('%Y%m%d'))
log_handler = RotatingFileHandler(filename=os.path.join(log_dir, log_name), maxBytes=20000, backupCount=5)
logging.basicConfig(handlers=[log_handler], level=logging.INFO,
                    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
                    datefmt='%Y-%m-%dT%H:%M:%S') 

def run():
    # auth = OAuthHandler(TwitterConfig.CONSUMER_KEY, TwitterConfig.CONSUMER_SECRET)
    # auth.set_access_token(TwitterConfig.ACCESS_TOKEN, TwitterConfig.ACCESS_TOKEN_SECRET)
    listener = TweetListener(TwitterConfig.CONSUMER_KEY, TwitterConfig.CONSUMER_SECRET, TwitterConfig.ACCESS_TOKEN, TwitterConfig.ACCESS_TOKEN_SECRET)
    listener.sample()
    logging.info('Starting stream for {}'.format(TwitterConfig.TWITTER_HANDLE))
    logging.info('Stream closed')

if __name__ == '__main__':
    run()