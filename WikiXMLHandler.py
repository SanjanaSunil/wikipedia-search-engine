#!/usr/bin/python3

import xml.sax
import multiprocessing
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
        self.docID = 0
        self.reset()

    def reset(self):
        self.currentTag = ""
        self.title = self.infobox = self.body = ""
        self.categories = self.references = self.externalLinks = ""
        self.infoboxFlag = self.referencesFlag = self.externalLinksFlag = 0
    

    def startElement(self, tag, attributes):
        self.currentTag = tag
        # if tag == "page":
        #     print("\n\n\n============== NEW PAGE STARTING! =============", self.docID)
    
    
    def endElement(self, tag):
        if tag == "page":
            # threading.Thread(target=self.test, args=()).start()
            # processor = TextProcessor()   
            self.textProcessor.processText(self.title, "title")
            self.textProcessor.processText(self.body, "text")
            self.textProcessor.processText(self.categories, "categories")
            self.textProcessor.processText(self.infobox, "infobox")
            self.textProcessor.processText(self.references, "references")
            self.textProcessor.processText(self.externalLinks, "external_links")
            
            self.textProcessor.createIndex(self.docID)
            # del processor
            self.docID += 1
            self.reset()

    
    def characters(self, content):
        if self.currentTag == "title":
            self.title += content
        elif self.currentTag == "text":
            if "[[Category:" in content or "[[category:" in content:
                pos = content.find("[[Category:")
                if pos == -1:
                    pos = content.find("[[category:")
                self.categories += content[pos:]
            elif "{{Infobox" in content or "{{infobox" in content:
                self.infoboxFlag = 1
                pos = content.find("{{Infobox")
                if pos == -1:
                    pos = content.find("{{infobox")
                content = content[pos:]
            elif "==Reference" in content or "== Reference" in content or "==reference" in content:
                self.referencesFlag = 1 
            elif "==External links==" in content or "== External links==" in content:
                self.externalLinksFlag = 1
            else:
                self.body += content

            if self.infoboxFlag >= 1:
                self.referencesFlag = 0
                self.externalLinksFlag = 0
                if "{{" in content:
                    self.infoboxFlag += 1
                if "}}" in content:
                    self.infoboxFlag -= 1
                if content == "}}":
                    self.infoboxFlag = 0
                self.infobox += content

            if self.referencesFlag == 1:
                self.infoboxFlag = 0
                self.externalLinksFlag = 0
                if self.references != "" and len(content) > 1 and content[0] != '{' and content[1] != '{':
                    self.referencesFlag = 0
                elif len(content) > 1 and content[0] == '{' and content[1] == '{':
                    self.references += content

            if self.externalLinksFlag == 1:
                self.infoboxFlag = 0
                self.referencesFlag = 0
                if self.externalLinks != "" and len(content) > 1 and content[0] != '{':
                    self.externalLinksFlag = 0
                elif len(content) > 0 and content[0] == '*':
                    self.externalLinks += content
