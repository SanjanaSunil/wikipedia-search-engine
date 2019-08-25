import os
import re
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

class Searcher():

    def __init__(self, path_to_index):
        self.sno = SnowballStemmer('english')
        self.stop_words = set(stopwords.words('english'))
        self.inverted_index = os.path.join(path_to_index, os.listdir(path_to_index)[0])    
    

    def binarySearchWord(self, f, word):
        f.seek(0, 2)
        l = 0 
        r = f.tell() - 1
        old_mid = -1
        new_mid = (l + r) >> 1

        while old_mid != new_mid and l <= r:
            old_mid = new_mid

            f.seek(new_mid)
            f.readline()
            word_offset = f.tell()
            line = f.readline()

            if not line or line.split('-', 1)[0] > word:
                r = new_mid - 1
            elif word == line.split('-', 1)[0]:
                return word_offset
            else:
                l = new_mid
            
            new_mid = (l + r) >> 1

        f.seek(0)
        line = f.readline()
        if word == line.split('-', 1)[0]:
            return 0

        return -1


    def processAndSearchQuery(self, query):
        query = query.lower()
        query_tokens = self.stem(self.removeStopWords(self.tokenize(query)))
        f = open(self.inverted_index, 'r')
        for query_token in query_tokens:
            print(self.binarySearchWord(f, query_token))
        f.close()


    def tokenize(self, text):
        text = text.replace("'", "").replace("_", "")
        tokens = re.findall(r"[\w']{3,}", text)
        return tokens


    def removeStopWords(self, tokens):
        tokens = [token for token in tokens if not token in self.stop_words]
        return tokens


    def stem(self, tokens):
        stemmedTokens = [self.sno.stem(token) for token in tokens]
        return stemmedTokens
