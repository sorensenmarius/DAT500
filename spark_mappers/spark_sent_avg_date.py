import sys
from operator import add
import pickle
import numpy as np
from statistics import mean
from pyspark.sql import SparkSession, dataframe



def mapper(line): 

    line = line[1:-1]
    
    try:
        id, string = line.split(',', 1)
    except:
        return
    id = id.strip("")
    id = int(id)

    string = string[2:-1]
    sentiment, date, gender ,_ = string.split(",",3)
        
    

    return (date , gender), float(sentiment)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Arguments: <input path> <output path>", file=sys.stderr)
        sys.exit(-1)

    spark = SparkSession\
        .builder\
        .appName('Date-Gender : Sentiment')\
        .master('spark://master:7077')\
        .config("spark.executor.memory", "6g")\
        .getOrCreate()

    lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])
    counts = lines.map(mapper) 
    sums =counts.groupByKey().mapValues(lambda x: sum(x) / len(x))

    sums.saveAsTextFile(sys.argv[2])

    spark.stop()
