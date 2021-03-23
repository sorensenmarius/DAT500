# %%
import pandas as pd
import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

# %%
tweets = pd.read_table('data/corona_tweets_01.csv',
                        names=['Sentiment'],
                        index_col=0,
                        sep=',')
# %%
tweet_ids = ','.join([str(item) for item in tweets.index[:10]])

# %%
headers = {'Authorization': f'Bearer {os.getenv("TWITTER_TOKEN")}'}
r = requests.get(f'https://api.twitter.com/2/tweets?ids={tweet_ids}', headers = headers)
response = json.loads(r.content)
d = response['data']
# %%
tweets['Text'] = ''

# %%
for tweet in d:
    tweets.loc[int(tweet['id']), 'Text'] = tweet['text']

tweets