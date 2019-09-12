import sys
import time
from Searcher import Searcher

if __name__ == '__main__':

    print("Initializing...")

    path_to_index = sys.argv[1]
    searcher = Searcher(path_to_index)

    print("Enter your query:\n")
    while 1:
        query = input()
        start_time = time.time()
        print(searcher.processAndSearchQuery(query))
        print("\nRESPONSE TIME: %s seconds" % (time.time() - start_time))
        print("====================")