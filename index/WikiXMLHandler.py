import xml.sax
import xml.etree.ElementTree as etree
from TextProcessor import TextProcessor

class WikiXMLParser():

    def __init__(self, xml_file, output_dir):
        self.textProcessor = TextProcessor()
        self.docID = 0
        self.output_dir = output_dir
        self.xml_file = xml_file
        self.reset()
    

    def reset(self):
        self.title = self.infobox = self.body = ""
        self.categories = self.references = self.externalLinks = ""
        self.infoboxFlag = self.referencesFlag = self.externalLinksFlag = 0
    

    def parse(self):
        for event, elem in etree.iterparse(self.xml_file, events=('start', 'end')):
            tag_name = elem.tag
            idx = tag_name.rfind("}")
            if idx != -1:
                tag_name = tag_name[idx + 1:]

            if event != 'start':
                if tag_name == 'title':
                    if elem.text:
                        self.textProcessor.processText(elem.text, "title")
                elif tag_name == 'text':
                    if elem.text:
                        sentences = elem.text.split('\n')
                        for sentence in sentences:
                            self.get_fields(sentence)
                elif tag_name == 'page':
                    self.textProcessor.processText(self.body, "text")
                    self.textProcessor.processText(self.categories, "categories")
                    self.textProcessor.processText(self.infobox, "infobox")
                    self.textProcessor.processText(self.references, "references")
                    self.textProcessor.processText(self.externalLinks, "external_links")
                    
                    self.textProcessor.createIndex(self.docID, self.output_dir)
                    self.docID += 1
                    self.reset()

                elem.clear()
    

    def get_fields(self, content):
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
