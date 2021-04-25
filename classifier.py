#%%
from math import nan
from nltk.corpus.reader.chasen import test
import pandas as pd
import numpy as np
import re
import nltk
from nltk import ngrams
import pickle
from scipy import sparse
nltk.download('punkt')
nltk.download('wordnet')


from yellowbrick.text import FreqDistVisualizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline



import warnings
warnings.filterwarnings("ignore")

#%%
trainData = pd.read_csv(r'data/gender-classifier-DFE-791531.csv',
                   encoding = "latin1")

# testData = pd.read_csv(r'data/blog-gender-dataset-clean.csv',names=["gender","description"],
                #    encoding = "utf-8")
#%%
data = trainData.loc[:,["gender", "text", "tweet_created"]]
data.dropna(axis = 0, inplace = True)
data.gender = [1 if gender == "female" else (0 if gender == "male" else 2 )for gender in data.gender]
#data.gender = [1 if gender == 'female' else 0 for gender in data.gender]
# testData.dropna(axis=0, inplace=True)
#%%
data.loc[data['gender'] == 2]
# %% natural language processing 
def nl_processing(data): 
    emoji_pat = '[\U0001F300-\U0001F64F\U0001F680-\U0001F6FF\u2600-\u26FF\u2700-\u27BF]'
    shrink_whitespace_reg = re.compile(r'\s{2,}')
    description_list = [] # we created a list so we after these steps, we will append into this list
    for description in data.text:
        try:
            #reg = re.compile(r'({})|[^a-zA-Z]'.format(emoji_pat)) # line a
            #result = reg.sub(lambda x: ' {} '.format(x.group(1)) if x.group(1) else ' ', description)
            #description =shrink_whitespace_reg.sub(' ', result)

            description = re.sub("[^a-zA-Z]", " ", description) # remove non letter signs 
            description = description.lower() 
            description = nltk.word_tokenize(description) # list of words
            lemma = nltk.WordNetLemmatizer() 
            description = [lemma.lemmatize(word) for word in description] # find orginal form of word ex. drove -> drive 
            description = " ".join(description) # join the words together and remake text.
            description_list.append(description) # and append these texts into the list we created.
        except:
            print(description)
            
    return description_list

#%%
description_list = nl_processing(data)
# description_list_test = nl_processing(testData)

# %%
# Bag of Words
def bag_words(description_list):
    max_features = 5000
    count_vectorizer = CountVectorizer(max_features=max_features,stop_words = "english", ngram_range=(1,2))
    sparce_matrix = count_vectorizer.fit_transform(description_list).toarray()
    features = count_vectorizer.get_feature_names()
    return sparce_matrix, features

#%%
sparce_matrix, features = bag_words(description_list)
pickle.dump(features, open('./reg_features.sav', 'wb'), protocol=2)

#%% visualize most freq words
visualizer = FreqDistVisualizer(features=features, orient='v', n = 10, color = "orange")
visualizer.fit(sparce_matrix)
visualizer.show()
# %%
y = data.iloc[:, 0].values
x = sparce_matrix
# y_test = testData.iloc[:, 0].values
# x_test,_ = bag_words(description_list_test)

# x_test.shape

# %% splits into train and test subset 
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.1, random_state = 42)
#%%

# %% Logistic regression
lr = LogisticRegression()
lr.fit(x_train, y_train)
print(lr.get_params)
print('Saving LR parameters')
pickle.dump(lr, open('./reg_params.sav', 'wb'))

y_pred = lr.predict(x_test)
accuracy = 100.0 * accuracy_score(y_test, y_pred)
print("Accuracy:{:.3%}".format(accuracy_score(y_test, y_pred)))

#%%
print('Loading LR parameters')
lr2 = pickle.load(open('./reg_params.sav', 'rb'))

y_pred = lr2.predict(x_test)
accuracy = 100.0 * accuracy_score(y_test, y_pred)
print("Accuracy:{:.3%}".format(accuracy_score(y_test, y_pred)))

#%%
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

dc = DecisionTreeClassifier(max_depth=10, min_samples_leaf = 1)
dc.fit(x,y)

#y_pred=dc.predict(x_test)

#accuracy = 100.0 * accuracy_score(y_test, y_pred)
#print("Accuracy:{:.3%}".format(accuracy_score(y_test, y_pred)))

pickle.dump(dc, open('./dc_params.sav', 'wb'),protocol=2)

#tree.plot_tree(dc)
#%%
features = pickle.load(open('./reg_features.sav', 'rb'))
lr = pickle.load(open('./dc_params.sav', 'rb'))
def classify_gender(x):
    #id, sentiment, text = x.split(",",2)
    text = x
    sparce_test = [feature in text for feature in features]
    sparce_test =np.array(sparce_test).astype(int).reshape(1,-1)
    return lr.predict(sparce_test)

#%%
blogData = pd.read_csv(r'data/blog-gender-dataset-clean.csv',names=["gender","text"],
                   encoding = "utf-8")
blogData
#%%
#blogData.dropna(axis = 0, inplace = True)
y_test = blogData.gender
cleanBlog = nl_processing(blogData)
testData = pd.read_csv(r'data/covid_tweet.csv',names=["id","sentiment","text"],encoding = "utf-8")
cleanTweets=nl_processing(testData)
test_pred =[]
for tweet in cleanBlog: 
    test_pred.append(classify_gender(tweet))

test_pred
accuracy = 100.0 * accuracy_score(y_test, test_pred)
print("Accuracy:{:.3%}".format(accuracy_score(y_test, test_pred)))



# %%
testData = pd.read_csv(r'data/combined.csv',names=["id","sentiment","text"],
                   encoding = "utf-8")
# %%
testData = testData[testData['text'].notna()]
# %%
cleanTest = nl_processing(testData)
# %%
test_pred =[]
for tweet in cleanTest: 
    test_pred.append(classify_gender(tweet))

testData.insert(3, 'gender', test_pred)
# %%
