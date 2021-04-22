import os
import glob
import pandas as pd
import sys

os.chdir('resulting_tweets')

if len(sys.argv) - 1 == 0 or sys.argv[1] == 'new':
    files = ['thread_1.csv', 'thread_2.csv', 'thread_3.csv']
elif sys.argv[1] == 'old':
    files = ['old_thread_1.csv', 'old_thread_2.csv', 'old_thread_3.csv']
elif sys.argv[1] == 'all':
    files = files = glob.glob('*.csv')

combined_csv = [pd.read_csv(f, index_col=None, sep=',', header=0) for f in files]

os.chdir('..')

for df in combined_csv:
    df.to_csv('combined.csv', mode='a', header=False, index=False)

print("successfylly combined CSV files")