from pyspark.sql import SparkSession
import sys

def mapper(line):
    _, string = line.split('\t')
    string = string.strip("\"")
    sentiment, date, _, _ = string.split(',',3)
    return date, float(sentiment)

if __name__ == '__main__': 
    if len(sys.argv[0] != 3):
        print('Usage: date_avg.py <input path> <ouput path>', file=sys.stderr)
        sys.exit(-1)
    
    spark = SparkSession\
        .builder\
        .appName('date_avg')\
        .master('spark://master:7077')\
        .config('spark.executor.memory', '6g')\
        .getOrCreate()

    lines = spark.read.text(sys.argv[0]).rdd.map(lambda r: r[0])
    mapped = lines.map(mapper) 
    average = mapped.groupByKey().mapValues(lambda x: sum(x)/ len(x))
    average.saveAsTextFile('average date', sys.argv[2])

    spark.stop()