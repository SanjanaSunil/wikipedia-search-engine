import heapq
import config

# Remember to delete all the files after each iteration

def kWayMerge(files, op_file):
    heap = []
    [heapq.heappush(heap, (file__.readline(), file__)) for file__ in files]

    prev_word = ""

    while(heap):
        smallest = heapq.heappop(heap)
        [cur_word, field_count] = smallest[0].split(':', 1)
        if cur_word == prev_word:
            op_file.write('|' + field_count.strip("\n"))
        else:
            if len(prev_word) == 0:
                op_file.write(smallest[0].strip("\n"))
            else:
                op_file.write('\n' + smallest[0].strip("\n"))
        prev_word = cur_word
        next_line = smallest[1].readline()
        if len(next_line) != 0:
            heapq.heappush(heap, (next_line, smallest[1]))


if __name__ == "__main__":

    op_file = open('output.txt', "w+") 

    files = []
    for i in range(0, 999):
        files.append(open(config.TEMP_INDICES_DIR + '/' + str(i) + '.txt', 'r'))
    
    kWayMerge(files, op_file)

    [file__.close() for file__ in files]