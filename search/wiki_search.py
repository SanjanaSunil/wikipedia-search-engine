import sys
import time
from Searcher import Searcher

if __name__ == '__main__':

    start_time = time.time()

    path_to_index = sys.argv[1]
    testfile = sys.argv[2]
    path_to_output = sys.argv[3]

    with open(testfile, 'r') as f:
        queries = f.readlines()

    outputs = []
    searcher = Searcher(path_to_index)
    for query in queries:
        outputs.append(searcher.processAndSearchQuery(query))
    
    with open(path_to_output, 'w') as f:
        for output in outputs:
            for line in output:
                f.write(line.strip() + '\n')
            f.write('\n')
    
    print("--- %s seconds ---" % (time.time() - start_time))