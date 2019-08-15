#!/usr/bin/python3

import xml.sax
from TextProcessor import TextProcessor

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
        self.infobox = ""
        self.body = ""
        self.categories = ""
    

    def startElement(self, tag, attributes):
        self.currentTag = tag
        if tag == "page":
            print("\n\n\n============== NEW PAGE STARTING! =============", self.docID)
    
    
    def endElement(self, tag):
        if tag == "page":
            self.textProcessor.createIndex(self.docID)
            self.docID += 1
        elif tag == "title":
            self.textProcessor.processText(self.title, tag)
            self.title = ""
        elif tag == "text":
            self.textProcessor.processText(self.body, tag)
            self.textProcessor.processText(self.categories, "categories")
            self.body = ""
            self.categories = ""
        self.currentTag = ""

    
    def characters(self, content):
        # if content == "==References==":
        if self.currentTag == "title":
            self.title += content
            # self.textProcessor.processText(content, self.currentTag)
        if self.currentTag == "text":
            if "[[Category:" in content:
                self.categories += content[11:]
            else:
                self.body += content


# ==References==
# {{Reflist}}

# [[Category:Churches in California]]
# [[Category:Buildings and structures in Siskiyou County, California]]
