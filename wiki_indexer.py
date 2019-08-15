#!/usr/bin/python3

import sys
import xml.sax
from WikiXMLHandler import WikiXMLHandler

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Usage: python3 <path-to-wiki-dump>")
        sys.exit(1)

    xmlFilePath = sys.argv[1]

    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    wikiHandler = WikiXMLHandler()
    parser.setContentHandler(wikiHandler)

    parser.parse(xmlFilePath)
