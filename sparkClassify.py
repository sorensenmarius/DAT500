import sys
from operator import add
import pickle
import numpy as np

from pyspark.sql import SparkSession, dataframe

features = pickle.load(open('./reg_features.sav', 'rb'))
lr = pickle.load(open('./dc_params.sav', 'rb'))


def mapper(line): 
    line = line[1:-1]

    try:
        id, string = line.split(',', 1)
    except:
        print('Ran into an error, the line is: ')
        print(line)
        return

    id = id.strip("")
    id = int(id)

    string = string[1:-1]
    sentiment, date, text = string.split(",",3)
        
    sparce_test = [feature in text for feature in features]
    sparce_test = np.array(sparce_test).astype(int).reshape(1,-1)

    gen_pred = lr.predict(sparce_test)[0]

    return id, f'{sentiment},{date},{gen_pred},{text}'


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: wordcount <file>", file=sys.stderr)
        sys.exit(-1)

    spark = SparkSession\
        .builder\
        .appName("Classify")\
        # .master('spark://master:7077')\
        .config("spark.executor.memory", "6g")\
        .getOrCreate()

    lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])
    counts = lines.map(mapper) 
    counts.saveAsTextFile(sys.argv[2])

    spark.stop()