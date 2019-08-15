#!/usr/bin/python3

import re

def processText(text, docID, tagType):
    """ Processes text according to title or body """
    text = text.lower()
    print(text)
    print(tokenize(text))


def tokenize(text):
    tokens = re.findall(r"[\w']+", text)
    return tokens