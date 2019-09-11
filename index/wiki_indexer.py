import os
import sys
import time
import xml.sax
import mergeFiles
from WikiXMLHandler import WikiXMLParser

if __name__ == "__main__":
    
    start_time = time.time()

    xmlFilePath = sys.argv[1]
    output_dir = sys.argv[2]

    wikiHandler = WikiXMLParser(xmlFilePath, output_dir)
    wikiHandler.parse()
    # parser = xml.sax.make_parser()
    # parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    # wikiHandler = WikiXMLHandler(output_dir)
    # parser.setContentHandler(wikiHandler)

    # parser.parse(xmlFilePath)
    mergeFiles.externalSort(output_dir)

    print("--- %s seconds ---" % (time.time() - start_time))
