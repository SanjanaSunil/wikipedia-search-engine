#!/usr/bin/python3

import re
import nltk
# from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords


class TextProcessor():

    def __init__(self):
        self.wordCount = {}
        self.stop_words = set(stopwords.words('english'))    
    

    def processText(self, text, tagType):
        """ Performs case folding, tokenisation and stemming """
        text = text.lower()
        tokens = self.stem(self.removeStopWords(self.tokenize(text)))
        # tokens = self.lemmatize(tokens)
        
        for token in tokens:
            if token not in self.wordCount:
                self.wordCount[token] = [0, 0, 0, 0, 0, 0]
            if tagType == "title":
                self.wordCount[token][0] += 1
            elif tagType == "text":
                self.wordCount[token][1] += 1
            elif tagType == "categories":
                self.wordCount[token][2] += 1
            elif tagType == "infobox":
                self.wordCount[token][3] += 1
            elif tagType == "references":
                self.wordCount[token][4] += 1
            elif tagType == "external_links":
                self.wordCount[token][5] += 1


    def createIndex(self, docID):
        sortedWords = sorted(self.wordCount.keys())
        print("\n\n\n============== NEW PAGE STARTING! =============", docID)
        print(docID)
        for word in sortedWords:
            print(word, " : ", self.wordCount[word])

        self.wordCount = {}


    def tokenize(self, text):
        tokens = re.findall(r"[\w']{2,}", text)
        tokens = [token.replace("'", "").replace("_", "") for token in tokens]
        return tokens

    def removeStopWords(self, tokens):
        tokens = [token for token in tokens if not token in self.stop_words]
        return tokens

    def stem(self, tokens):
        sno = nltk.stem.SnowballStemmer('english')
        # porter = PorterStemmer()
        stemmedTokens = [sno.stem(token) for token in tokens]
        return stemmedTokens


    def lemmatize(self, tokens):
        lemmatizer = WordNetLemmatizer()
        lemmatizedTokens = [lemmatizer.lemmatize(token) for token in tokens]
        return lemmatizedTokens
