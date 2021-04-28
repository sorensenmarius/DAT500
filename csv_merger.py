import os
import glob
import pandas as pd
import sys

os.chdir('resulting_tweets')

if len(sys.argv) - 1 == 0 or sys.argv[1] == 'new':
    files = glob.glob('thread_?.csv')
elif sys.argv[1] == 'old':
    files = glob.glob('old_thread_?.csv')
elif sys.argv[1] == 'all':
    files = glob.glob('*.csv')
elif sys.argv[1] == 'random':
    files = glob.glob('random_thread_?.csv')
elif sys.argv[1] == 'fullRandom':
    files = glob.glob('random_thread_?.csv') + ['../../dis_materials/combined.csv']

combined_csv = [pd.read_csv(f, index_col=None, sep=',', header=0, engine='python', encoding='utf-8', error_bad_lines=False) for f in files]

os.chdir('..')

for df in combined_csv:
    df.to_csv('random_combined.csv', mode='a', header=False, index=False)

print("successfylly combined CSV files")