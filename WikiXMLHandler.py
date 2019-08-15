#!/usr/bin/python3

import xml.sax

class WikiXMLHandler(xml.sax.ContentHandler):
    
    """
    Handler for parsing Wikipedia XML data
    ...

    Attributes
    ----------
    CurrentTag : string
        Tag being currently processed

    docID : int
        New ID of article being processed

    Other attributes store content of the corresponding tag
    """

    def __init__(self):
        self.CurrentTag = ""
        self.docID = 0
        self.title = ""
        self.text = ""
    

    def startElement(self, tag, attributes):
        self.CurrentTag = tag
        if tag == "page":
            print("NEW PAGE STARTING!", self.docID)
    
    
    def endElement(self, tag):
        if tag == "page":
            self.docID += 1
        elif tag == "title":
            print(self.title)
            self.title = ""
        elif tag == "text":
            self.text = ""
        self.CurrentTag = ""

    
    def characters(self, content):
        if self.CurrentTag == "title":
            self.title += content
        # elif self.CurrentTag == "text":
        #     self.text += content
