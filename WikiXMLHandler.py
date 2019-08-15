#!/usr/bin/python3

import xml.sax
import processCorpus

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
        self.currentTag = ""
        self.docID = 0
        self.title = ""
        self.text = ""
    

    def startElement(self, tag, attributes):
        self.currentTag = tag
        if tag == "page":
            print("NEW PAGE STARTING! =========", self.docID)
    
    
    def endElement(self, tag):
        if tag == "page":
            self.docID += 1
        elif tag == "title":
            self.title = ""
        elif tag == "text":
            self.text = ""
        self.currentTag = ""

    
    def characters(self, content):
        if self.currentTag == "title":
            processCorpus.processText(content, self.docID, self.currentTag)
            self.title += content
        # elif self.currentTag == "text":
        #     self.text += content
