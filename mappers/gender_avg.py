from mrjob.job import MRJob
from statistics import mean

class MRGenderAvg(MRJob):

    def mapper(self,_,line):
        _, string = line.split('\t')
        string = string.strip("\"")
        sentiment, _, gender, _ = string.split(',',3)
        yield gender, float(sentiment)

    def reducer(self, key, values):
        yield key, mean(values)


if __name__ == '__main__': 
    MRGenderAvg.run()
