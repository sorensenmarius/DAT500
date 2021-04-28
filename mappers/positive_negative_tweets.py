from mrjob.job import MRJob
from statistics import mean


class PositiveNegativeTweets(MRJob):
    def mapper(self,_,line):
        _, string = line.split('\t')
        string = string.strip("\"")
        sentiment, date, _, _ = string.split(',',3)
        sent = 'negative'
        if float(sentiment) != 0 and float(sentiment) > 0:
            sent = 'positive'
        yield (date, sent), 1

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__': 
    PositiveNegativeTweets.run()
