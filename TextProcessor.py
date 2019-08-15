#!/usr/bin/python3

import re
from collections import OrderedDict
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer 


class TextProcessor():

    def __init__(self):
        self.titleWordCount = {}
        self.bodyWordCount = {}
    

    def processText(self, text, tagType):
        """ Performs case folding, tokenisation and stemming """
        text = text.lower()
        tokens = self.stem(self.removeStopWords(self.tokenize(text)))
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


    def createIndex(self, docID):
        sortedTitleWords = sorted(self.titleWordCount.keys())
        sortedBodyWords = sorted(self.bodyWordCount.keys())

        print(docID)
        
        i = 0
        j = 0
        while i < len(sortedTitleWords) and j < len(sortedBodyWords):
            if sortedTitleWords[i] < sortedBodyWords[j]:
                val = self.titleWordCount[sortedTitleWords[i]]
                print(sortedTitleWords[i], " : ", val)
                i += 1
            elif sortedBodyWords[j] < sortedTitleWords[i]:
                val = self.bodyWordCount[sortedBodyWords[j]]
                print(sortedBodyWords[j], " : ", val)
                j += 1
            else:
                val1 = self.titleWordCount[sortedTitleWords[i]]
                val2 = self.bodyWordCount[sortedBodyWords[j]]
                print(sortedTitleWords[i], " : ", val1 + val2)
                i += 1
                j += 1
        while i < len(sortedTitleWords):
            val = self.titleWordCount[sortedTitleWords[i]]
            print(sortedTitleWords[i], " : ", val)
            i += 1
        while j < len(sortedBodyWords):
            val = self.bodyWordCount[sortedBodyWords[j]]
            print(sortedBodyWords[j], " : ", val)
            j += 1

        self.titleWordCount = {}
        self.bodyWordCount = {}


    def tokenize(self, text):
        tokens = re.findall(r"[\w']+", text)
        tokens = [token.replace("'", "").replace("_", "") for token in tokens]
        return tokens

    def removeStopWords(self, tokens):
        tokens = [token for token in tokens if len(token) > 1]
        return tokens

    def stem(self, tokens):
        porter = PorterStemmer()
        stemmedTokens = [porter.stem(token) for token in tokens]
        return stemmedTokens


    def lemmatize(self, tokens):
        lemmatizer = WordNetLemmatizer()
        lemmatizedTokens = [lemmatizer.lemmatize(token) for token in tokens]
        return lemmatizedTokens
