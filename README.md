# Twitter Analysis Dashboard using Streamlit, Tweepy and Engagement API

This script extracts, processes and stores tweets using Twitter API given the user access keys. To implement the script, user should first apply for the access within Twitter API:
1. General Twitter API
2. Engagement API (possible to apply as organization)

To start up the application:
1. Clone the repository
2. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.

```bash
pip install -r requirements.txt
```
# Setup

The credentials are split into two seperate files:
1. Twitter regular API credentials are stored in .env file. Create a .env file and store the credentials as follows:

```
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = '' 
TWITTER_HANDLE = ''
DB_USER = ''
DB_PWORD = ''
DB_HOST = ''
```

2. (Optional) Twitter Enterprise API credentials are stored in .twitter_api_creds. Create a .twitter_api_creds file and store the credentials as follows:

```
username: YOUR_USER_NAME
engagement:
    consumer_key: --
    consumer_secret: --
    token: --
    token_secret: --
    url: https://data-api.twitter.com/insights/engagement
```

# Usage
1. Run the following command in your terminal to initialize the application. This script will gather all historic tweets given a certain handle (as per setup)

```bash
python initialize_app.py
```

2. Set up the streamer to keep adding new tweets in real-time

```bash
python run_streamer.py
```

3. Finally, start the streamlit app to open up the dashboard

```bash
streamlit run app.py
```
The dashboard should now be available at localhost (and should open up automatically)