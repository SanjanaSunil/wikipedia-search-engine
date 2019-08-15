#!/usr/bin/python3

import xml.sax

class WikiXMLHandler(xml.sax.ContentHandler):
    
    """
    Handler for parsing Wikipedia XML data
    ...

    Attributes
    ----------
    CurrentTag : string
        Indicates current tag

    Other attributes store content of the corresponding tag
    """

    def __init__(self):
        self.CurrentTag = ""
        self.title = ""
        self.text = ""
    

    def startElement(self, tag, attributes):
        self.CurrentTag = tag
        if tag == "page":
            print("NEW PAGE STARTING!")
    
    
    def endElement(self, tag):
        if self.CurrentTag == "title":
            print(self.title)
            self.title = ""
        elif self.CurrentTag == "text":
            self.text = ""
        self.CurrentTag = ""

    
    def characters(self, content):
        if self.CurrentTag == "title":
            self.title += content
        # elif self.CurrentTag == "text":
        #     self.text += content
