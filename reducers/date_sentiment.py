from mrjob.job import MRJob

class DateSentiment(MRJob):
    def reducer(self, key, values):
        print(f'Key: {key}, Values: {values}')
    
if __name__ == '__main__': 
    DateSentiment.run()