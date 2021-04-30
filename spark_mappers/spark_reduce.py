import sys
from operator import add
import pickle
import numpy as np
from statistics import mean
from pyspark.sql import SparkSession, dataframe



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: wordcount <file>", file=sys.stderr)
        sys.exit(-1)

    spark = SparkSession\
        .builder\
        .appName("Classify")\
        .master('spark://master:7077')\
        .config("spark.executor.memory", "6g")\
        .getOrCreate()

    lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])
    cleanData = lines.filter(lambda x : x != 'None')

    cleanData.saveAsTextFile(sys.argv[2])

    spark.stop()
