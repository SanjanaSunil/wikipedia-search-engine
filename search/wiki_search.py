import sys
from Searcher import Searcher

if __name__ == '__main__':

    path_to_index = sys.argv[1]
    testfile = sys.argv[2]
    path_to_output = sys.argv[3]

    with open(testfile, 'r') as file:
        queries = file.readlines()

    # outputs = []
    # for query in queries:
    #     outputs.append(query)
    # write_file(outputs, path_to_output)



def write_file(outputs, path_to_output):
    '''outputs should be a list of lists.
        len(outputs) = number of queries
        Each element in outputs should be a list of titles corresponding to a particular query.'''
    with open(path_to_output, 'w') as file:
        for output in outputs:
            for line in output:
                file.write(line.strip() + '\n')
            file.write('\n')