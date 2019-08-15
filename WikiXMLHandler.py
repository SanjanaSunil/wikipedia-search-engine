#!/usr/bin/python3

import xml.sax

class WikiXMLHandler(xml.sax.ContentHandler):
    
    """
    Handler for parsing Wikipedia XML data
    ...

    Attributes
    ----------
    CurrentData : string
        Indicates current tag

    Other attributes store content of the corresponding tag
    """

    def __init__(self):
        self.CurrentData = ""
        self.title = ""
    

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "page":
            print("NEW PAGE STARTING!")
    
    
    def endElement(self, tag):
        if self.CurrentData == "title":
            print(self.title)
        self.CurrentData = ""

    
    def characters(self, content):
        if self.CurrentData == "title":
            self.title = content



if __name__ == "__main__":
    
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    Handler = WikiXMLHandler()
    parser.setContentHandler(Handler)

    parser.parse("../wiki.xml")
