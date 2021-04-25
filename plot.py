# %%
import plotly.express as px
import pandas as pd
from statistics import mean

# %%
df = px.data.tips()
df
# fig = px.histogram(df, x="total_bill", color="sex")
# fig.show()
# %%
date_gender_sentiment = pd.read_csv('reduced_data/gender_date_sentiment.csv', '\t', names=['DateAndGender', 'Sentiment'])
date_gender_sentiment['DateAndGender'] = date_gender_sentiment['DateAndGender'].str.replace('\[|\]|\"', '')
date_gender_sentiment[['Date', 'Gender']] = date_gender_sentiment['DateAndGender'].str.split(',', 1, expand=True)
date_gender_sentiment.drop(columns=['DateAndGender'])
fig = px.line(date_gender_sentiment, x="Date", y='Sentiment',color="Gender")
fig.show()

# %%
date_gender_sentiment = pd.read_csv('reduced_data/gender_date_count.csv', '\t', names=['DateAndGender', 'Count'])
date_gender_sentiment['DateAndGender'] = date_gender_sentiment['DateAndGender'].str.replace('\[|\]|\"', '')
date_gender_sentiment[['Date', 'Gender']] = date_gender_sentiment['DateAndGender'].str.split(',', 1, expand=True)
date_gender_sentiment.drop(columns=['DateAndGender'])
fig = px.line(date_gender_sentiment, x="Date", y='Count',color="Gender")
fig.show()
# %%
fig = px.bar(date_gender_sentiment, x="Date", y='Count',color="Gender")
fig.show()

# %%
fig = px.histogram(date_gender_sentiment, x="Date", y='Count',color="Gender")
fig.show()
# %%
date_gender_sentiment = pd.read_csv('reduced_data/random_gender_date_sentiment.csv', '\t', names=['DateAndGender', 'Sentiment'])
date_gender_sentiment['DateAndGender'] = date_gender_sentiment['DateAndGender'].str.replace('\[|\]|\"', '')
date_gender_sentiment[['Date', 'Gender']] = date_gender_sentiment['DateAndGender'].str.split(',', 1, expand=True)
date_gender_sentiment.drop(columns=['DateAndGender'])
date_gender_sentiment['Gender'].replace('0', 'Male', inplace=True)
date_gender_sentiment['Gender'].replace('1', 'Female', inplace=True)
fig = px.histogram(date_gender_sentiment, x="Date", y='Sentiment',color="Gender",histfunc='avg')
fig.show()
fig = px.bar(date_gender_sentiment, x="Date", y='Sentiment',color="Gender")
fig.show()
fig = px.line(date_gender_sentiment, x="Date", y='Sentiment',color="Gender")
fig.show()
# %%
mean(date_gender_sentiment['Sentiment'])
# %%
positive_negative = pd.read_csv('reduced_data/random_positive_negative.csv', '\t', names=['DateAndOpinion', 'Count'])
positive_negative['DateAndOpinion'] = positive_negative['DateAndOpinion'].str.replace('\[|\]|\"', '')
positive_negative[['Date', 'Opinion']] = positive_negative['DateAndOpinion'].str.split(',', 1, expand=True)
positive_negative.drop(columns=['DateAndOpinion'], inplace=True)

g = positive_negative.groupby('Date').sum()
for i, row in positive_negative.iterrows():
    positive_negative.at[i, 'RelativeFrequency'] = row['Count'] / g['Count'][row['Date']]

fig = px.histogram(positive_negative, x="Date", y='RelativeFrequency',color="Opinion",histfunc='avg')
fig.show()
fig = px.bar(positive_negative, x="Date", y='RelativeFrequency',color="Opinion")
fig.show()
fig = px.line(positive_negative, x="Date", y='RelativeFrequency',color="Opinion")
fig.show()

# %%
