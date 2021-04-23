#! /usr/bin/python

import pickle
import numpy as np
from mrjob.job import MRJob

class MRClassify(MRJob):
    def mapper(self,_, line): 
        id, sentiment, text, time = line.split(",",2)
        features = pickle.load(open('./reg_features.sav', 'rb'))

        sparce_test = [feature not in text for feature in features]
        sparce_test =np.array(sparce_test).astype(int).reshape(1,-1)
        lr = pickle.load(open('./dc_params.sav', 'rb'))
        gen_pred = lr.predict(sparce_test)

        yield text, [gen_pred,sentiment,time]
        # yield [text,sentiment,time] , gen_pred

    # def reducer(self, key, values):
    #     yield key, values

if __name__ == '__main__': 
    MRClassify.run()