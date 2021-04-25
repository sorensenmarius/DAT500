import pickle
import numpy as np
import sys
from mrjob.job import MRJob

class MRClassify(MRJob):
    features = pickle.load(open('./reg_features.sav', 'rb'))
    lr = pickle.load(open('./dc_params.sav', 'rb'))

    def mapper(self,_, line):
        id, string = line.split('\t', 1)
        id = id.strip("")
        id = int(id)
        string = string.strip("\"")
        sentiment, date, text = string.split(",",3)
        
        sparce_test = [feature in text for feature in self.features]
        sparce_test = np.array(sparce_test).astype(int).reshape(1,-1)

        gen_pred = self.lr.predict(sparce_test)[0]


        yield id, f'{sentiment},{date},{gen_pred},{text}'

    # def reducer(self, key, values):
    #     yield key, values

if __name__ == '__main__':
    MRClassify.run()