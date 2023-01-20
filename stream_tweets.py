from models import Tweet
import tweepy
import sqlite3
from config import TwitterConfig
import logging

logger = logging.getLogger(__name__)


class TweetListener(tweepy.Stream):

    def on_status(self, status):
        if status.user.id_str != TwitterConfig.TWITTER_HANDLE:
            return
        tweet = Tweet(tweet_id=status.id_str, created_at=status.created_at, likes=status.favourites_count, impressions=0, engagement_rate=0, retweets=status.retweet_count, quote_tweets=0, replies=0, link_clicks=0, video_views=0, profile_clicks=0, hashtags='', pc_likes=0, pc_impressions=0, pc_engagement_rate=0)
        self.insert_tweet(tweet)

    def on_error(self, status_code):
        if status_code == 420:
            # Stream limit reached, need to close the stream
            logger.warning('Limit Reached. Closing stream ({})'.format(TwitterConfig.TWITTER_HANDLE))
            return False
        logger.warning('Streaming error (status code {})'.format(status_code))

    def insert_tweet(self, tweet):
        try:
            with self.con as sess:
                sess.add(tweet)
        except Exception as e:
            logger.warning('Unable to insert tweet: {}'.format(e))
