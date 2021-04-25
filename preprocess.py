from mrjob.job import MRJob
from datetime import datetime
import re
import nltk

class MRPreprocess(MRJob):
    def mapper(self, _, line): 
        split=line.split(",",2)

        try:
            id = int(split[0])
        except:
            return
        

        if len(split) != 3:
            return

        _, sentiment, text = split 

        emoji_pat = '[\U0001F300-\U0001F64F\U0001F680-\U0001F6FF\u2600-\u26FF\u2700-\u27BF]'
        shrink_whitespace_reg = re.compile(r'\s{2,}')
        reg = re.compile(r'({})|[^a-zA-Z]'.format(emoji_pat)) # line a
        result = reg.sub(lambda x: ' {} '.format(x.group(1)) if x.group(1) else ' ', text)
        description = shrink_whitespace_reg.sub(' ', result)

        #description = re.sub("[^a-zA-Z]", " ", description) # remove non letter signs 
        description = description.lower() 
        description = nltk.word_tokenize(description) # list of words
        lemma = nltk.WordNetLemmatizer() 
        description = [lemma.lemmatize(word) for word in description] # find orginal form of word ex. drove -> drive 
        description = " ".join(description) 

        shifted = id >> 22 
        timestamp = shifted + 1288834974657
        time_created = datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d')

        string = f'{sentiment},{time_created},{description}'

        yield id, string
    
    # def reduce(self, key, values): 
    #     string = f'{key},{values[0][0]},{values[0][1]},{values[0][2]}'
    #     yield string

if __name__ == '__main__': 
    MRPreprocess.run()




