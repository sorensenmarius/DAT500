# Gender and Sentiment analysis using tweets - COVID-19
This repository contains Python scripts to be able to run analysis on a dataset containing tweet IDs and sentiment values. 

## How to run
The `hadoop_commands.txt` file contains more commands for running the code both locally and on a distributed Hadoop cluster. The main idea is as follows:

1. Download tweet data from the Twitter API using `get_tweets.py` or `get_tweets_multithread.py`
2. Merge the tweets to a single file using `csv_merger.py`
3. Preprocess the data using `preprocess.py`. This can be run on a Hadoop cluster.
4. Classify the gender of each tweet using `classify.py`. This can also be run on a Hadoop cluster. If you would like you can train your own classifier using `classifier.py`
5. Use the different mappers in the `mappers` folder to gain information from the data. These can also be run on a Hadoop cluster.