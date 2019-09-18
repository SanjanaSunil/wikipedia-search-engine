import os
import re
import math
import heapq
from operator import itemgetter
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

class Searcher():

    def __init__(self, path_to_index):
        self.sno = SnowballStemmer('english')
        self.stop_words = set(stopwords.words('english'))

        self.index_path = path_to_index

        self.inverted_indices = []
        for f in os.listdir(path_to_index):
            if f != 'titles.txt' and f != 'extra.txt':
                self.inverted_indices.append(f)
        self.inverted_indices.sort()

        # self.inverted_index = os.path.join(path_to_index, 'inverted_index.txt')
        self.titles = os.path.join(path_to_index, 'titles.txt')

        f = open(os.path.join(path_to_index, 'extra.txt'), "r")
        self.total_docs = int(f.readline())
        f.close()
    

    def binarySearchIndex(self, word):
        l = 0
        r = len(self.inverted_indices) - 1
        ans = -1

        while l <= r:
            mid = (l + r) // 2
            if self.inverted_indices[mid] <= word:
                ans = mid
                l = mid + 1
            else:
                r = mid - 1

        if ans == -1 or ans >= len(self.inverted_indices) or self.inverted_indices[ans] > word:
            return ""        
        return self.inverted_indices[ans]


    def binarySearchWord(self, f, word, inp_type): 
        f.seek(0, 2)
        l = 0 
        r = f.tell() - 1
        old_mid = -1
        new_mid = (l + r) >> 1

        while old_mid != new_mid and l <= r:
            old_mid = new_mid

            f.seek(new_mid)
            f.readline()
            line = f.readline()

            doc_word = line.split('-', 1)[0]
            if inp_type == "integer":
                doc_word = int(doc_word)
        
            if not line or doc_word > word:
                r = new_mid - 1
            elif word == doc_word:
                return line.rstrip('\n').split('-', 1)[1]
            else:
                l = new_mid
            
            new_mid = (l + r) >> 1

        f.seek(0)
        line = f.readline()
        if word == line.split('-', 1)[0]:
            return line.rstrip('\n').split('-', 1)[1]

        return ""


    def getTopNResults(self, docID_heap, n):
        prev_docID = -1
        cnt = 0
        cnt_heap = []

        limit = 5000
        while docID_heap and limit:
            smallest = heapq.heappop(docID_heap)
            next_info = smallest[1].split('|', 1)
            if len(next_info) > 1:
                [docID, field_cnt] = next_info[1].split('d', 1)
                heapq.heappush(docID_heap, (int(docID), field_cnt, smallest[2]))
                limit -= 1
            if smallest[0] == prev_docID:
                if smallest[2] == '-':
                    if cnt == 0:
                        cnt = 1
                    cnt *= sum([int(i) for i in re.findall(r'\d+', next_info[0])])
                elif smallest[2][0] in next_info[0]:
                    if cnt == 0:
                        cnt = 1
                    _, rest = next_info[0].split(smallest[2][0])
                    cnt *= (int(re.search(r'\d+', rest).group()) + 1)
            else:
                heapq.heappush(cnt_heap, (-cnt, prev_docID))
                prev_docID = smallest[0]
                if smallest[2] == '-':
                    cnt = sum([int(i) for i in re.findall(r'\d+', next_info[0])])
                elif smallest[2][0] in next_info[0]:
                    _, rest = next_info[0].split(smallest[2][0])
                    cnt = int(re.search(r'\d+', rest).group())
                else:
                    cnt = 0
        
        if cnt > 0:
            heapq.heappush(cnt_heap, (-cnt, prev_docID))
        
        f = open(self.titles, encoding="utf8", errors='ignore')
        while cnt_heap and n:
            smallest = heapq.heappop(cnt_heap)
            result = self.binarySearchWord(f, smallest[1], "integer")
            if result.rstrip() != "":
                print(result)
            n -= 1
        f.close()


    def calculateTFIDF(self, query_vector, docs_vectors, posting, query_idx, field):
        docs_info = posting.split('|', 150000)[:149999]
        total_doc_words = 0
        if field == '-':
            total_doc_words = len(docs_info)
        else:
            for info in docs_info:
                if field[0] in info:
                    total_doc_words += 1        
        if total_doc_words == 0:
            return
            
        idf = math.log10(self.total_docs/total_doc_words)

        for info in docs_info:
            [docID, field_cnt] = info.split('d', 1)
            tf = 0
            if field == '-':
                tf = sum([int(i) for i in re.findall(r'\d+', field_cnt)])
            else:
                field_info = field_cnt.split(field[0])
                if len(field_info) > 1:
                    tf = int(re.search(r'\d+', field_info[1]).group())
                if field[0] == 't':
                    tf *= 20
            if tf != 0:
                if docID not in docs_vectors:
                    docs_vectors[docID] = [0] * len(query_vector)
                docs_vectors[docID][query_idx] = tf * idf

        query_vector[query_idx] *= idf


    def calculateCosineSim(self, query_vector, doc_vector):
        dot_prod = 0
        for i in range(len(query_vector)):
            dot_prod += (query_vector[i] * doc_vector[i])
        
        # query_dist = math.sqrt(sum(map(lambda x:x*x, query_vector)))
        doc_dist = math.sqrt(sum(map(lambda x:x*x, doc_vector)))
        return dot_prod/math.sqrt(doc_dist)


    def getRankedResults(self, query_vector, docs_vectors, n):
        heap = []
        for docID in docs_vectors:
            doc_vector = docs_vectors[docID]
            doc_wgt = sum(x > 0 for x in doc_vector) * self.calculateCosineSim(query_vector,doc_vector)
            heapq.heappush(heap, (-doc_wgt, int(docID)))

        f = open(self.titles, encoding="utf8", errors='ignore')
        while heap and n > 0:
            smallest = heapq.heappop(heap)
            print(self.binarySearchWord(f, smallest[1], "integer"))
            n -= 1
        f.close()


    def getDuplicateCount(self, query_tokens):
        uniq_tokens = []
        query_vector = []
        for query_token in query_tokens:
            flag = -1
            for j, uniq_token in enumerate(uniq_tokens):
                if query_token == uniq_token:
                    flag = j
                    break
            if flag == -1:
                uniq_tokens.append(query_token)
                query_vector.append(1)
            else:
                query_vector[j] += 1
        return uniq_tokens, query_vector


    def calculateOneWordRank(self, posting, n, field):
        docs = posting.split('|', 1500000)[:1499999]
        docs_cnt = []
        for doc in docs:
            [docID, field_cnt] = doc.split('d', 1)
            if field == "-":
                docs_cnt.append((sum([int(i) for i in re.findall(r'\d+', field_cnt)]), docID))
            elif field[0] in field_cnt:
                _, rest = field_cnt.split(field[0])
                docs_cnt.append((int(re.search(r'\d+', rest).group()), docID))
        
        docs_cnt = sorted(docs_cnt, key=itemgetter(0), reverse=True)[:n]

        f = open(self.titles, encoding="utf8", errors='ignore')
        for doc in docs_cnt:
            result = self.binarySearchWord(f, int(doc[1]), "integer")
            if result.rstrip() != "":
                print(result)
        f.close()


    def processAndSearchQuery(self, query):
        query = query.lower()
        query_tokens = self.stem(self.removeStopWords(self.tokenize(query)))

        query_tokens, query_vector = self.getDuplicateCount(query_tokens)
        docs_vectors = {}
        # heap = []

        for i, query_token in enumerate(query_tokens):
            inverted_index = self.binarySearchIndex(query_token[0])

            if inverted_index != "":
                index_file = os.path.join(self.index_path, inverted_index)
                f = open(index_file, encoding="utf8", errors='ignore')
                posting = self.binarySearchWord(f, query_token[0], "string")
                if posting != "":
                    if len(query_tokens) == 1:
                        self.calculateOneWordRank(posting, 10, query_token[1])
                        return
                        # [docID, field_cnt] = posting.split('d', 1) 
                        # heapq.heappush(heap, (int(docID), field_cnt, query_token[1]))
                    else:
                        self.calculateTFIDF(query_vector, docs_vectors, posting, i, query_token[1])
                f.close()

        # if len(query_tokens) == 1:
        #     self.getTopNResults(heap, 10)
        # else:
        self.getRankedResults(query_vector, docs_vectors, 10)


    def tokenize(self, text):
        text = text.replace("'", "").replace("_", "")
        tokens = re.findall(r"[\w':]{3,}", text)
        tokensAndFields = []
        for token in tokens:
            tokenAndField = token.split(':', 1)
            if len(tokenAndField) == 1:
                tokensAndFields.append([tokenAndField[0], '-'])
            else:
                tokensAndFields.append([tokenAndField[1], tokenAndField[0]])
        return tokensAndFields


    def removeStopWords(self, tokensAndFields):
        tokens = [token for token in tokensAndFields if not token[0] in self.stop_words]
        return tokens


    def stem(self, tokensAndFields):
        stemmedTokens = [[self.sno.stem(token[0]), token[1]] for token in tokensAndFields]
        return stemmedTokens
