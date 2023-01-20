from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from database import Base

col_names = ['tweet_id',
        'created_at',
        'likes',
        'impressions',
        'engagement_rate',
        'retweets',
        'quote_tweets',
        'replies',
        'link_clicks',
        'video_views',
        'profile_clicks',
        'hashtags',
        'pc_likes',
        'pc_impressions',
        'pc_engagement_rate']

class Tweet(Base):
    __tablename__ = 'tweets'
    tweet_id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    likes = Column(Integer)
    impressions = Column(Integer)
    engagement_rate = Column(Float)
    retweets = Column(Integer)
    quote_tweets = Column(Integer)
    replies = Column(Integer)
    link_clicks = Column(Integer)
    video_views = Column(Integer)
    profile_clicks = Column(Integer)
    hashtags = Column(String(500))
    pc_likes = Column(Float)
    pc_impressions = Column(Float)
    pc_engagement_rate = Column(Float)

    def __init__(self, tweet_id, created_at, likes, impressions, engagement_rate, retweets, quote_tweets, replies, link_clicks, video_views, profile_clicks, hashtags, pc_likes, pc_impressions, pc_engagement_rate):
        tweet_id = tweet_id
        created_at = created_at
        likes = likes
        impressions = impressions
        engagement_rate = engagement_rate
        retweets = retweets
        quote_tweets = quote_tweets
        replies = replies
        link_clicks = link_clicks
        video_views = video_views
        profile_clicks = profile_clicks
        hashtags = hashtags
        pc_likes = pc_likes
        pc_impressions = pc_impressions
        pc_engagement_rate = pc_engagement_rate

    def __repr__(self):
        return '<Tweet %r>' % self.body