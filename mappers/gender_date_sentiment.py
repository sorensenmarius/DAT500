from mrjob.job import MRJob
from statistics import mean

class GenderDateSentiment(MRJob):
    def mapper(self,_,line):
        _, string = line.split('\t')
        string = string.strip("\"")
        sentiment, date, gender, _ = string.split(',',3)
        # if float(sentiment) != 0:
        yield (date, gender), float(sentiment)

    def reducer(self, key, values):
        yield key, mean(values)


if __name__ == '__main__': 
    GenderDateSentiment.run()
