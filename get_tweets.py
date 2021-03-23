# %%
import pandas as pd
import requests
import os
from dotenv import load_dotenv
import json
from tqdm import tqdm
load_dotenv()

# %%
tweets = pd.read_table('data/corona_tweets_01.csv',
                        names=['Sentiment'],
                        index_col=0,
                        sep=',')
# %%
tweets['Text'] = ''
headers = {'Authorization': f'Bearer {os.getenv("TWITTER_TOKEN")}'}
for i in tqdm(range(100)):
    tweet_ids = ','.join([str(item) for item in tweets.index[100 * i:100 * (i + 1)]])
    r = requests.get(f'https://api.twitter.com/2/tweets?ids={tweet_ids}', headers = headers)
    try:
        response = json.loads(r.content)
        if 'data' in response:
            d = response['data']
            for tweet in d:
                tweets.loc[int(tweet['id']), 'Text'] = tweet['text']

# %%
tweets