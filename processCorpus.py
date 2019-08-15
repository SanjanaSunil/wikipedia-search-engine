#!/usr/bin/python3

import re
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer 

def processText(text, docID, tagType):
    """ Processes text according to title or body """
    text = text.lower()
    print(text)
    text = stem(tokenize(text))
    # text = lemmatize(text)
    print(text)


def tokenize(text):
    tokens = re.findall(r"[\w']+", text)
    tokens = [token.replace("'", "") for token in tokens]
    return tokens


def stem(tokens):
    porter = PorterStemmer()
    stemmedTokens = [porter.stem(token) for token in tokens]
    return stemmedTokens


def lemmatize(tokens):
    lemmatizer = WordNetLemmatizer()
    lemmatizedTokens = [lemmatizer.lemmatize(token) for token in tokens]
    return lemmatizedTokens
