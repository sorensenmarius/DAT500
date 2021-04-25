from mrjob.job import MRJob

class GenderDayCount(MRJob):

    def mapper(self,_,line):
        _, string = line.split('\t')
        string = string.strip("\"")
        _, date, gender, _ = string.split(',',3)
        yield (date, gender), 1

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__': 
    GenderDayCount.run()
