import sys
import time
from Searcher import Searcher

if __name__ == '__main__':

    print("Initializing...")

    path_to_index = sys.argv[1]
    searcher = Searcher(path_to_index)

    print("Enter your query:\n")
    while 1:
        print("QUERY: ", end='')
        query = input()
        print()
        start_time = time.time()
        searcher.processAndSearchQuery(query)
        print("\nRESPONSE TIME: %s seconds" % (time.time() - start_time))
        print("====================")