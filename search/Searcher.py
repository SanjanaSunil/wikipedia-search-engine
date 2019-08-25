import os
import re
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

class Searcher():

    def __init__(self, path_to_index):
        self.sno = SnowballStemmer('english')
        self.stop_words = set(stopwords.words('english'))
        self.inverted_index = os.path.join(path_to_index, os.listdir(path_to_index)[0])
        self.offsets = os.path.join(path_to_index, 'offsets.txt')
    

    def binarySearchWord(self, word):
        offsets_f = open(self.offsets)

    def processAndSearchQuery(self, query):
        query = query.lower()
        query_tokens = self.stem(self.removeStopWords(self.tokenize(query)))
        


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
