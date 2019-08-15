#!/usr/bin/python3

import re
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer 


class TextProcessor():

    def __init__(self):
        self.titleWordCount = {}
        self.bodyWordCount = {}
    

    def processText(self, text, tagType):
        """ Performs case folding, tokenisation and stemming """
        text = text.lower()
        tokens = self.stem(self.tokenize(text))
        # tokens = lemmatize(tokens)
        
        for token in tokens:

            if tagType == "title":
                if token not in self.titleWordCount:
                    self.titleWordCount[token] = 0
                self.titleWordCount[token] += 1

            elif tagType == "text":
                if token not in self.bodyWordCount:
                    self.bodyWordCount[token] = 0
                self.bodyWordCount[token] += 1


    def createIndex(self):
        print(self.titleWordCount)
        print(self.bodyWordCount)
        self.titleWordCount = {}
        self.bodyWordCount = {}


    def tokenize(self, text):
        tokens = re.findall(r"[\w']+", text)
        tokens = [token.replace("'", "") for token in tokens]
        return tokens


    def stem(self, tokens):
        porter = PorterStemmer()
        stemmedTokens = [porter.stem(token) for token in tokens]
        return stemmedTokens


    def lemmatize(self, tokens):
        lemmatizer = WordNetLemmatizer()
        lemmatizedTokens = [lemmatizer.lemmatize(token) for token in tokens]
        return lemmatizedTokens
