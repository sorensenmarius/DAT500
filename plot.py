# %%
import plotly.express as px
import pandas as pd

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