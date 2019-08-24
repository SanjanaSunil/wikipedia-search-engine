import os
import heapq
import config

def kWayMerge(files, op_file):
    heap = []
    prev_word = ""
    [heapq.heappush(heap, (f.readline(), f)) for f in files]

    while heap:
        smallest = heapq.heappop(heap)
        [cur_word, field_count] = smallest[0].split('-', 1)
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


def externalSort():

    max_files = config.MAX_OPEN_FILES - 10
    cur_dir = config.TEMP_INDICES_DIR

    iter_no = 0

    while os.path.exists(cur_dir + '/1-' + str(iter_no) + '.txt'):

        new_file_id = 0
        files_left_flag = 1

        while files_left_flag:
            files = []
            unwanted_files = []
            start = new_file_id * max_files
            end = start + max_files

            for i in range(start, end):
                try:
                    files.append(open(cur_dir + '/' + str(i) + '-' + str(iter_no) + '.txt', 'r'))
                except:
                    files_left_flag = 0
                    break
                unwanted_files.append(cur_dir + '/' + str(i) + '-' + str(iter_no) + '.txt')
            
            if len(files) == 0:
                break

            op_file = open(cur_dir + '/' + str(new_file_id) + '-' + str(iter_no+1) + '.txt', "w+") 
            kWayMerge(files, op_file)
            [f.close() for f in files]
            [os.remove(unwanted_file) for unwanted_file in unwanted_files]
            new_file_id += 1
            op_file.close()
        
        iter_no += 1
