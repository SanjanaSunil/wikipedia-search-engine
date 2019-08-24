import os
import sys
import time
import config
import xml.sax
import mergeFiles
from WikiXMLHandler import WikiXMLHandler

if __name__ == "__main__":
    
    start_time = time.time()

    os.mkdir(config.TEMP_INDICES_DIR)

    xmlFilePath = sys.argv[1]

    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    wikiHandler = WikiXMLHandler()
    parser.setContentHandler(wikiHandler)

    parser.parse(xmlFilePath)
    mergeFiles.externalSort()

    # inverted_index = os.listdir(config.TEMP_INDICES_DIR)
    # os.rename(config.TEMP_INDICES_DIR + '/' + inverted_index, config.TEMP_INDICES_DIR + '/' + 'index.txt')

    print("--- %s seconds ---" % (time.time() - start_time))
