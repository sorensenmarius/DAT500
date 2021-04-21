#%%
import pandas as pd
import re
import nltk


from yellowbrick.text import FreqDistVisualizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


import warnings
warnings.filterwarnings("ignore")

#%%
trainData = pd.read_csv(r'data/gender-classifier-DFE-791531.csv',
                   encoding = "utf-8")

testData = pd.read_csv(r'data/blog-gender-dataset-clean.csv',names=["gender","description"],
                   encoding = "utf-8")
#%%
data = trainData.loc[:,["gender", "description", "tweet_created"]]
data.dropna(axis = 0, inplace = True)
data.gender = [1 if gender == "female" else 0 for gender in data.gender]

testData.dropna(axis=0, inplace=True)
data
# %% natural language processing 
def nl_processing(data): 
    emoji_pat = '[\U0001F300-\U0001F64F\U0001F680-\U0001F6FF\u2600-\u26FF\u2700-\u27BF]'
    shrink_whitespace_reg = re.compile(r'\s{2,}')
    description_list = [] # we created a list so we after these steps, we will append into this list
    for description in data.description:
        reg = re.compile(r'({})|[^a-zA-Z]'.format(emoji_pat)) # line a
        result = reg.sub(lambda x: ' {} '.format(x.group(1)) if x.group(1) else ' ', description)
        description =shrink_whitespace_reg.sub(' ', result)

        #description = re.sub("[^a-zA-Z]", " ", description) # remove non letter signs 
        description = description.lower() 
        description = nltk.word_tokenize(description) # list of words
        lemma = nltk.WordNetLemmatizer() 
        description = [lemma.lemmatize(word) for word in description] # find orginal form of word ex. drove -> drive 
        description = " ".join(description) # join the words together and remake text.
        description_list.append(description) # and append these texts into the list we created.
    return description_list

#%%
description_list = nl_processing(data)
description_list_test = nl_processing(testData)

description_list
# %%
# Bag of Words
def bag_words(description_list):
    max_features = 5000
    count_vectorizer = CountVectorizer(max_features=max_features,stop_words = "english")
    sparce_matrix = count_vectorizer.fit_transform(description_list).toarray()
    features = count_vectorizer.get_feature_names()
    return sparce_matrix, features

#%%
sparce_matrix, features = bag_words(description_list)

#%% visualize most freq words
visualizer = FreqDistVisualizer(features=features, orient='v', n = 10, color = "orange")
visualizer.fit(sparce_matrix)
visualizer.show()
# %%
y = data.iloc[:, 0].values
x = sparce_matrix
#y_test = testData.iloc[:, 0].values
#x_test,_ = bag_words(description_list_test)

#x_test.shape

# %% splits into train and test subset 
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.1, random_state = 42)
#%%

# %% Logistic regression
lr = LogisticRegression(random_state = 42)
lr.fit(x_train, y_train)
y_pred = lr.predict(x_test)
accuracy = 100.0 * accuracy_score(y_test, y_pred)
print("Accuracy:{:.3%}".format(accuracy_score(y_test, y_pred)))
# %%
# Random Forest Implementation

rf = RandomForestClassifier()
rf.fit(x, y)
# prediction
y_pred = rf.predict(x_test)
# Random Forest 
accuracy = 100.0 * accuracy_score(y_test, y_pred)
print("Accuracy: ", accuracy)

#%%
from sklearn.neighbors import KNeighborsClassifier
rf = KNeighborsClassifier()
rf.fit(x, y)
# prediction
y_pred = rf.predict(x_test)
# Random Forest 
accuracy = 100.0 * accuracy_score(y_test, y_pred)
print("Accuracy: ", accuracy)

