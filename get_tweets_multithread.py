# %%
from dotenv import load_dotenv
import json
import os
import pandas as pd
import requests
import threading

load_dotenv()

# %%
def get_tweets(token):
    for filename in os.listdir(f'data/combined_{token[-1]}'):
        if filename.endswith(".csv"):

            tweets = pd.read_table(f"data/combined_{token[-1]}/{filename}",
                                names=['Sentiment'],
                                index_col=0,
                                sep=',')

            tweets['Text'] = ''
            headers = {'Authorization': f'Bearer {os.getenv(token)}'}
            
            try:
                df_inner = pd.DataFrame(columns=['id','Sentiment', 'Text'])
                df_inner.set_index('id')
            except Exception as e:
                print("Error creating dataframe: ", e)

            for i in range(len(tweets)):
                tweet_ids = ','.join([str(item) for item in tweets.index[100 * i:100 * (i + 1)]])
                r = requests.get(f'https://api.twitter.com/2/tweets?ids={tweet_ids}', headers = headers)
                try:
                    response = json.loads(r.content)
                    if 'data' in response:
                        d = response['data']
                        for tweet in d:
                            df_inner = df_inner.append({'id': tweet['id'],
                                             'Sentiment': tweets.loc[int(tweet['id']), 'Sentiment'],
                                             'Text': tweet['text']
                                            }, ignore_index=True)
                except Exception as e:
                    print("Error on adding response to inner dataframe: ", e)

                if i % 10000 == 0:
                    df_inner.to_csv(f'resulting_tweets/thread_{token[-1]}.csv', mode='a', header=False, index=False)
                    df_inner = pd.DataFrame(columns=['id', 'Sentiment', 'Text'])
                    df_inner.set_index('id')

# %%
try:
   T1 = threading.Thread(target=get_tweets, args=('TWITTER_TOKEN_1',))
   T1.start()
   T2 = threading.Thread(target=get_tweets, args=('TWITTER_TOKEN_2',))
   T2.start()
   T3 = threading.Thread(target=get_tweets, args=('TWITTER_TOKEN_3',))
   T3.start()
except:
   print("Error: unable to start thread")

# %%
