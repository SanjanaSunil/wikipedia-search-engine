import xml.sax
import os
import resource
import mergeFiles
from TextProcessor import TextProcessor

class WikiXMLHandler(xml.sax.ContentHandler):
    
    """
    Handler for parsing Wikipedia XML data
    ...

    Attributes
    ----------
    docID : int
        New ID of article being processed

    textProcessor: TextProcessor
        Performs case-folding, tokenisation and stemming and creates inverted index

    Other attributes contain content of corresponding tag
    e.g. self.title contains title name

    Methods
    -------
    startElement()
        Checks and sets current tag
    endElement()
        At the ending of an article, processes text and creates inverted index
    characters()
        Checks each line and adds cintent to corresponding tag attributes
    reset()
        Resets all tag attributes to empty string

    """

    def __init__(self, output_dir):
        self.textProcessor = TextProcessor()
        self.docID = 0
        self.output_dir = output_dir
        self.MAX_OPEN_FILES = resource.getrlimit(resource.RLIMIT_NOFILE)[0] - 20
        self.new_merge = 0
        self.reset()


    def reset(self):
        self.currentTag = ""
        self.title = self.infobox = self.body = ""
        self.categories = self.references = self.externalLinks = ""
        self.infoboxFlag = self.referencesFlag = self.externalLinksFlag = 0
    

    def startElement(self, tag, attributes):
        self.currentTag = tag 
    
    
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
            
            self.textProcessor.createIndex(self.docID, self.output_dir)
            # del processor
            self.docID += 1
            self.reset()

            if self.docID % self.MAX_OPEN_FILES == 0 and self.docID > 0:
                self.mergeInitialFiles()


    def mergeInitialFiles(self):
        start = self.new_merge * self.MAX_OPEN_FILES
        end = self.docID
        if end <= start:
            return

        files = []
        unwanted_files = []
        for i in range(start, end):
            files.append(open(self.output_dir + '/' + str(i) + '-0.txt', encoding='utf-8', errors='ignore'))
            unwanted_files.append(self.output_dir + '/' + str(i) + '-0.txt')
        
        op_file = open(self.output_dir + '/' + str(self.new_merge) + '-1.txt', "w+", encoding='utf-8')
        mergeFiles.kWayMerge(self.output_dir, files, op_file, False)

        [f.close() for f in files]
        [os.remove(unwanted_file) for unwanted_file in unwanted_files]
        self.new_merge += 1
        op_file.close()
    

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
