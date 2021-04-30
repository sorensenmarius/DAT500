from pyspark.sql import SparkSession
import sys

def mapper(line):
    _, string = line.split('\t')
    string = string.strip("\"")
    _, date, gender, _ = string.split(',',3)
    return (date, gender), 1

if __name__ == '__main__': 
    if len(sys.argv[0] != 3):
        print('Usage: gender_date_count.py <input path> <ouput path>', file=sys.stderr)
        sys.exit(-1)
    
    spark = SparkSession\
        .builder\
        .appName('gender_date_count')\
        .master('spark://master:7077')\
        .config('spark.executor.memory', '6g')\
        .getOrCreate()

    lines = spark.read.text(sys.argv[0]).rdd.map(lambda r: r[0])
    mapped = lines.map(mapper) 
    summed = mapped.groupByKey().mapValues(sum)
    summed.saveAsTextFile(sys.argv[2])

    spark.stop()