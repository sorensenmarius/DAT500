
import sys
from operator import add
import pickle
import re
from datetime import datetime
import nltk
from pyspark.sql import SparkSession
import numpy as np

features = pickle.load(open('./reg_features.sav', 'rb'))
lr = pickle.load(open('./dc_params.sav', 'rb'))


def mapper(line): 
        split=line.split(",",2)

        try:
            id = int(split[0])
        except:
            return
        

        if len(split) != 3:
            return

        _, sentiment, text = split 

        emoji_pat = '[\U0001F300-\U0001F64F\U0001F680-\U0001F6FF\u2600-\u26FF\u2700-\u27BF]'
        shrink_whitespace_reg = re.compile(r'\s{2,}')
        reg = re.compile(r'({})|[^a-zA-Z]'.format(emoji_pat)) # line a
        result = reg.sub(lambda x: ' {} '.format(x.group(1)) if x.group(1) else ' ', text)
        description = shrink_whitespace_reg.sub(' ', result)

        #description = re.sub("[^a-zA-Z]", " ", description) # remove non letter signs 
        description = description.lower() 
        description = nltk.word_tokenize(description) # list of words
        lemma = nltk.WordNetLemmatizer() 
        description = [lemma.lemmatize(word) for word in description] # find orginal form of word ex. drove -> drive 
        description = " ".join(description) 

        shifted = id >> 22 
        timestamp = shifted + 1288834974657
        time_created = datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d')

        sparce_test = [feature in description for feature in features]
        sparce_test = np.array(sparce_test).astype(int).reshape(1,-1)

        gen_pred = lr.predict(sparce_test)[0]

        string = f'{sentiment},{time_created},{gen_pred},{description}'

        return id, string

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: wordcount <file>", file=sys.stderr)
        sys.exit(-1)

    spark = SparkSession\
        .builder\
        .appName("PythonWordCount")\
        .getOrCreate()

    lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])
    counts = lines.map(mapper) 
    counts.saveAsTextFile(sys.argv[2])

    spark.stop()
