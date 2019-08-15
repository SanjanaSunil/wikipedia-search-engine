#!/usr/bin/python3

import xml.sax
from processCorpus import TextProcessor

class WikiXMLHandler(xml.sax.ContentHandler):
    
    """
    Handler for parsing Wikipedia XML data
    ...

    Attributes
    ----------
    currentTag : string
        Tag being currently processed

    docID : int
        New ID of article being processed

    Other attributes store content of the corresponding tag
    """

    def __init__(self):
        self.textProcessor = TextProcessor()
        self.currentTag = ""
        self.docID = 0
        self.title = ""
        self.text = ""
    

    def startElement(self, tag, attributes):
        self.currentTag = tag
        if tag == "page":
            print("\n\n\n==============NEW PAGE STARTING! =============", self.docID)
    
    
    def endElement(self, tag):
        if tag == "page":
            self.textProcessor.createIndex()
            self.docID += 1
        elif tag == "title":
            self.title = ""
        elif tag == "text":
            self.text = ""
        self.currentTag = ""

    
    def characters(self, content):
        if self.currentTag == "title" or self.currentTag == "text":
            self.textProcessor.processText(content, self.currentTag)
