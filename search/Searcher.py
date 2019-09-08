import os
import re
import math
import heapq
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

class Searcher():

    def __init__(self, path_to_index):
        self.sno = SnowballStemmer('english')
        self.stop_words = set(stopwords.words('english'))
        self.inverted_index = os.path.join(path_to_index, 'inverted_index.txt')
        self.titles = os.path.join(path_to_index, 'titles.txt')

        f = open(os.path.join(path_to_index, 'extra.txt'), "r")
        self.total_docs = int(f.readline())
        f.close()
    

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

        while docID_heap:
            smallest = heapq.heappop(docID_heap)
            next_info = smallest[1].split('|', 1)
            if len(next_info) > 1:
                [docID, field_cnt] = next_info[1].split('d', 1)
                heapq.heappush(docID_heap, (int(docID), field_cnt, smallest[2]))
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
        
        results = []
        f = open(self.titles, encoding="utf8", errors='ignore')
        while cnt_heap and n:
            smallest = heapq.heappop(cnt_heap)
            result = self.binarySearchWord(f, smallest[1], "integer")
            if result.rstrip() != "":
                results.append(result)
            n -= 1
        f.close()
        return results


    def calculateTFIDF(self, query_vector, docs_vectors, posting, query_idx):
        docs_info = posting.split('|')
        total_doc_words = len(docs_info)
        idf = math.log10(self.total_docs/total_doc_words)

        for info in docs_info:
            [docID, field_cnt] = info.split('d', 1)
            tf = sum([int(i) for i in re.findall(r'\d+', field_cnt)])
            if docID not in docs_vectors:
                docs_vectors[docID] = [0] * len(query_vector)
            docs_vectors[docID][query_idx] = tf * idf

        query_vector[query_idx] *= idf


    def calculateCosineSim(self, query_vector, doc_vector):
        dot_prod = 0
        for i in range(len(query_vector)):
            dot_prod += (query_vector[i] * doc_vector[i])
        
        query_dist = math.sqrt(sum(map(lambda x:x*x, query_vector)))
        doc_dist = math.sqrt(sum(map(lambda x:x*x, doc_vector)))
        return dot_prod/(query_dist*doc_dist)


    def getRankedResults(self, query_vector, docs_vectors, n):
        ranked_docs = []
        heap = []
        for docID in docs_vectors:
            heapq.heappush(heap, (-self.calculateCosineSim(query_vector,docs_vectors[docID]), int(docID)))

        f = open(self.titles, encoding="utf8", errors='ignore')
        while heap and n > 0:
            smallest = heapq.heappop(heap)
            ranked_docs.append(self.binarySearchWord(f, smallest[1], "integer"))
            n -= 1
        f.close()

        return ranked_docs


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


    def processAndSearchQuery(self, query):
        query = query.lower()
        query_tokens = self.stem(self.removeStopWords(self.tokenize(query)))

        query_tokens, query_vector = self.getDuplicateCount(query_tokens)
        docs_vectors = {}
        heap = []

        f = open(self.inverted_index, encoding="utf8", errors='ignore')
        for i, query_token in enumerate(query_tokens):
            posting = self.binarySearchWord(f, query_token[0], "string")
            if posting != "":
                if len(query_tokens) == 1:
                    [docID, field_cnt] = posting.split('d', 1) 
                    heapq.heappush(heap, (int(docID), field_cnt, query_token[1]))
                else:
                    self.calculateTFIDF(query_vector, docs_vectors, posting, i)
        f.close()

        if len(query_tokens) == 1:
            return self.getTopNResults(heap, 10)
        else:
            return self.getRankedResults(query_vector, docs_vectors, 10)


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
