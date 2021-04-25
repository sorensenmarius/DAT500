from mrjob.job import MRJob
from statistics import mean


class MRDateAvg(MRJob):
    def mapper(self,_,line):
        _, string = line.split('\t')
        string = string.strip("\"")
        sentiment, date, _, _ = string.split(',',3)
        yield date, float(sentiment)

    def reducer(self, key, values):
        yield key, mean(values)


if __name__ == '__main__': 
    MRDateAvg.run()
