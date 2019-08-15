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
        
        print(sortedTitleWords)
        print(sortedBodyWords)
        print(self.titleWordCount)
        print(self.bodyWordCount)
        # print(docID)
        # i = 0
        # j = 0
        # while i < len(sortedTitleWords) and j < len(sortedBodyWords):
        #     if sortedTitleWords[i] < sortedBodyWords[j]:
        #         print(sortedTitleWords[i], " : ", self.titleWordCount[sortedTitleWords[i]])
        #         i += 1
        #     elif sortedBodyWords[j] < sortedTitleWords[i]:
        #         print(sortedBodyWords[j], " : ", self.bodyWordCount[sortedBodyWords[j]])
        #         j += 1
        #     else:
        #         print(sortedTitleWords[i], " : ", self.titleWordCount[sortedTitleWords[i]] + self.bodyWordCount[sortedBodyWords[j]])
        #         i += 1
        #         j += 1
        # while i < len(sortedTitleWords):
        #     print(sortedTitleWords[i], " : ", self.titleWordCount[sortedTitleWords[i]])
        #     i += 1
        # while j < len(sortedBodyWords):
        #     if sortedTitleWords[i] > sortedBodyWords[j]:
        #         print(sortedBodyWords[j], " : ", self.bodyWordCount[sortedBodyWords[j]])
        #         j += 1

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
