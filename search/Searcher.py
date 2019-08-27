import os
import re
import heapq
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

class Searcher():

    def __init__(self, path_to_index):
        self.sno = SnowballStemmer('english')
        self.stop_words = set(stopwords.words('english'))
        self.inverted_index = os.path.join(path_to_index, 'inverted_index.txt')
        self.titles = os.path.join(path_to_index, 'titles.txt')
    

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
        prev_docID = "-1"
        cnt = 0
        cnt_heap = []

        while docID_heap:
            smallest = heapq.heappop(docID_heap)
            next_info = smallest[1].split('|', 1)
            if len(next_info) > 1:
                [docID, field_cnt] = next_info[1].split('d', 1)
                heapq.heappush(docID_heap, (docID, field_cnt))
            if smallest[0] == prev_docID:
                cnt += 1
            else:
                heapq.heappush(cnt_heap, (-1*cnt, prev_docID))
                prev_docID = smallest[0]
                cnt = 1
        
        if cnt > 0:
            heapq.heappush(cnt_heap, (-cnt, prev_docID))
        
        results = []
        f = open(self.titles, encoding="utf8", errors='ignore')
        while cnt_heap and n:
            smallest = heapq.heappop(cnt_heap)
            results.append(self.binarySearchWord(f, int(smallest[1].rstrip()), "integer"))
            n -= 1
        f.close()
        return results


    def processAndSearchQuery(self, query):
        query = query.lower()
        query_tokens = self.stem(self.removeStopWords(self.tokenize(query)))
        
        heap = []
        f = open(self.inverted_index, encoding="utf8", errors='ignore')
        for query_token in query_tokens:
            posting = self.binarySearchWord(f, query_token, "string")
            if posting != "":
                [docID, field_cnt] = posting.split('d', 1) 
                heapq.heappush(heap, (docID, field_cnt))
        f.close()
        
        return self.getTopNResults(heap, 10)


    def tokenize(self, text):
        text = text.replace("'", "").replace("_", "")
        tokens = re.findall(r"[\w']{3,}", text)
        return tokens


    def removeStopWords(self, tokens):
        tokens = [token for token in tokens if not token in self.stop_words]
        return tokens


    def stem(self, tokens):
        stemmedTokens = [self.sno.stem(token) for token in tokens]
        return stemmedTokens
