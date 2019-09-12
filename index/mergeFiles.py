import os
import heapq
import resource

def kWayMerge(op_dir, files, op_file, last_iter):
    heap = []
    prev_word = ""

    for f in files:
        line = f.readline()
        [word, word_info] = line.split('-', 1)
        [docID, field_cnt] = word_info.split('d', 1)
        heapq.heappush(heap, (word, int(docID), field_cnt, f))
    
    word_cnt = 0

    while heap:
        smallest = heapq.heappop(heap)
        if not last_iter:
            if smallest[0] == prev_word:
                op_file.write('|' + str(smallest[1]) + 'd' + smallest[2].strip("\n"))
            else:
                if len(prev_word) == 0:
                    op_file.write(smallest[0].strip("\n") + '-' + str(smallest[1]) + 'd' + smallest[2].strip("\n"))
                else:
                    op_file.write('\n' + smallest[0].strip("\n") + '-' + str(smallest[1]) + 'd' + smallest[2].strip("\n"))
        else:
            if smallest[0] == prev_word:
                last_file.write('|' + str(smallest[1]) + 'd' + smallest[2].strip("\n"))
            else:
                if word_cnt > 1000000:
                    last_file.close()
                    word_cnt = 0
                if word_cnt == 0:
                    last_file = open(op_dir + '/' + smallest[0], "w+", encoding='utf-8')
                if word_cnt == 0:
                    last_file.write(smallest[0].strip("\n") + '-' + str(smallest[1]) + 'd' + smallest[2].strip("\n"))
                else:
                    last_file.write('\n' + smallest[0].strip("\n") + '-' + str(smallest[1]) + 'd' + smallest[2].strip("\n"))
                word_cnt += 1            

        prev_word = smallest[0]
        next_line = smallest[3].readline()
        if len(next_line) != 0:
            [word, word_info] = next_line.split('-', 1)
            [docID, field_cnt] = word_info.split('d', 1)
            heapq.heappush(heap, (word, int(docID), field_cnt, smallest[3]))


def externalSort(output_dir):

    max_files = resource.getrlimit(resource.RLIMIT_NOFILE)[0] - 10
    cur_dir = output_dir

    iter_no = 1

    while os.path.exists(cur_dir + '/1-' + str(iter_no) + '.txt'):

        new_file_id = 0
        files_left_flag = 1

        last_iter = False
        if not os.path.exists(os.path.join(cur_dir, str(max_files) + '-' + str(iter_no) + '.txt')):
            last_iter = True

        while files_left_flag:
            files = []
            unwanted_files = []
            start = new_file_id * max_files
            end = start + max_files

            for i in range(start, end):
                try:
                    files.append(open(cur_dir + '/' + str(i) + '-' + str(iter_no) + '.txt', encoding='utf-8', errors='ignore'))
                except:
                    files_left_flag = 0
                    break
                unwanted_files.append(cur_dir + '/' + str(i) + '-' + str(iter_no) + '.txt')
            
            if len(files) == 0:
                break

            if last_iter:
                unwanted_files.append(cur_dir + '/' + str(new_file_id) + '-' + str(iter_no+1) + '.txt')

            op_file = open(cur_dir + '/' + str(new_file_id) + '-' + str(iter_no+1) + '.txt', "w+", encoding='utf-8') 
            kWayMerge(cur_dir, files, op_file, last_iter)
            [f.close() for f in files]
            [os.remove(unwanted_file) for unwanted_file in unwanted_files]
            new_file_id += 1
            op_file.close()
        
        iter_no += 1
    
    # src = os.path.join(cur_dir, '0-' + str(iter_no) + '.txt')
    # dest = os.path.join(cur_dir, 'inverted_index.txt')
    # os.rename(src, dest)