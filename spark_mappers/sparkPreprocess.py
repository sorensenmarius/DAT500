
import sys
from operator import add
import pickle
import re
from datetime import datetime
import nltk
from pyspark.sql import SparkSession


def mapper(line, nltk):
        nltk.download('punkt')
        nltk.download('wordnet')

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

        string = f'{sentiment},{time_created},{description}'

        return id, string

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: preprocess.py <input path> <output path>", file=sys.stderr)
        sys.exit(-1)

    features = pickle.load(open('./reg_features.sav', 'rb'))
    lr = pickle.load(open('./dc_params.sav', 'rb'))

    spark = SparkSession\
        .builder\
        .appName("Preprocess")\
        .master('spark://master:7077')\
        .config("spark.executor.memory", "6g")\
        .getOrCreate()

    lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])
    counts = lines.map(lambda x: mapper(x, nltk)) 
    counts.saveAsTextFile(sys.argv[2])

    spark.stop()
