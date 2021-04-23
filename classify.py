#! /usr/bin/python

# import pickle
import numpy as np
import sys

import zipimport
importer = zipimport.zipimporter('mrjob_numpy_yaml.zip')
mrjob = importer.load_module('mrjob')
job = importer.load_module('mrjob/job')

class MRClassify(job.MRJob):
    def mapper(self,_, line):
        sys.stderr.write('Line: ' + line)
        # id, sentiment, text = line.split(",",2)
        # features = pickle.load(open('./reg_features.sav', 'rb'))

        # sparce_test = [feature not in text for feature in features]
        # sparce_test = np.array(sparce_test).astype(int).reshape(1,-1)
        # lr = pickle.load(open('./reg_params.sav', 'rb'))
        # gen_pred = lr.predict(sparce_test)
        gen_pred = 'HATER NORSKE BOKSTAVER'
        text = 'yeet'

        yield text, [gen_pred,sentiment]

    def reducer(self, key, values):
        yield key, values

if __name__ == '__main__':
    MRClassify.run()
