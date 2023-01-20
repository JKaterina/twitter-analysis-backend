import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from contextlib import contextmanager

engine = sqlite3.connect("data/twitter_data.sqlite", check_same_thread=False)
Session = scoped_session(sessionmaker(autocommit=False, bind=engine))
Base = declarative_base()