#!/usr/bin/python3

import os
import sys
import time
import config
import xml.sax
import mergeFiles
from WikiXMLHandler import WikiXMLHandler

if __name__ == "__main__":
    
    start_time = time.time()

    if len(sys.argv) != 2:
        print("Usage: python3 <path-to-wiki-dump>")
        sys.exit(1)

    os.mkdir(config.TEMP_INDICES_DIR)

    xmlFilePath = sys.argv[1]

    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    wikiHandler = WikiXMLHandler()
    parser.setContentHandler(wikiHandler)

    parser.parse(xmlFilePath)

    mergeFiles.externalSort()

    print("--- %s seconds ---" % (time.time() - start_time))
