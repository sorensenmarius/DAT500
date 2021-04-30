import sys
from operator import add
import pickle
import numpy as np
from statistics import mean
from pyspark.sql import SparkSession, dataframe



def pos_neg(line):
    line = line[1:-1]

    id, string = line.split(',', 1)
   
    id = id.strip("")
    id = int(id)

    string = string[2:-1]
    sentiment, date, gender ,_ = string.split(",",3)

    sent = 'negative'
    if float(sentiment) != 0 and float(sentiment) > 0:
        sent = 'positive'
    return (date, sent), 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Arguments: <input path> <output path>", file=sys.stderr)
        sys.exit(-1)

    spark = SparkSession\
        .builder\
        .appName("Classify")\
        .master('spark://master:7077')\
        .config("spark.executor.memory", "1g")\
        .getOrCreate()

    lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])
    counts = lines.map(pos_neg) 
    sums =counts.groupByKey().mapValues(lambda x: sum(x))

    sums.saveAsTextFile(sys.argv[2])

    spark.stop()
