import re
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer 

class TextProcessor():

    """
    Takes in text, processes it and writes inverted indices to file
    ...

    Attributes
    ----------
    wordCount : dict
        Maps word to an array of size 6 with count of title, text, infobox,
        categories, references and external links
    
    sno : SnowBallStemmer
        Stems words
    
    stop_words : set
        Stop words in nltk

    """

    def __init__(self):
        self.wordCount = {}
        self.sno = SnowballStemmer('english')
        self.stop_words = set(stopwords.words('english'))
        self.title = ""


    def processText(self, text, tagType):
        """ Performs case folding, tokenisation and stemming """
        if tagType == "title":
            self.title = text.rstrip().rstrip('\n')
        text = text.lower()
        tokens = self.stem(self.removeStopWords(self.tokenize(text)))
        # tokens = self.lemmatize(tokens)
        for token in tokens:
            if token not in self.wordCount:
                self.wordCount[token] = [0, 0, 0, 0, 0, 0]
            if tagType == "title":
                self.wordCount[token][0] += 1
            elif tagType == "text":
                self.wordCount[token][1] += 1
            elif tagType == "infobox":
                self.wordCount[token][2] += 1
            elif tagType == "categories":
                self.wordCount[token][3] += 1
            elif tagType == "references":
                self.wordCount[token][4] += 1
            elif tagType == "external_links":
                self.wordCount[token][5] += 1


    def createIndex(self, docID, output_dir):
        """ Creates inverted index """ 
        sortedWords = sorted(self.wordCount.keys())
        f = open(output_dir + "/" + str(docID) + '-0.txt', "w+")
        for word in sortedWords:
            fieldString = ""
            fieldCount = self.wordCount[word]
            totalCount = sum(fieldCount)
            if fieldCount[0] > 0:
                fieldString += 't' + str(fieldCount[0])
            if fieldCount[1] > 0:
                fieldString += 'b' + str(fieldCount[1])
            if fieldCount[2] >  0:
                fieldString += 'i' + str(fieldCount[2])
            if fieldCount[3] >  0:
                fieldString += 'c' + str(fieldCount[3])
            if fieldCount[4] >  0:
                fieldString += 'r' + str(fieldCount[4])
            if fieldCount[5] >  0:
                fieldString += 'e' + str(fieldCount[5])        
            f.write(word + '-' + str(docID) + 'd' + str(totalCount) + fieldString + '\n')     
        f.close()
        self.wordCount = {}
        f = open(output_dir + "/titles.txt", "a+")
        if docID == 0:
            f.write(str(docID) + '-' + self.title)
        else:
            f.write('\n' + str(docID) + '-' + self.title)
        f.close()


    def tokenize(self, text):
        text = text.replace("'", "").replace("_", "")
        tokens = re.findall(r"[\w']{3,}", text)
        return tokens

    def removeStopWords(self, tokens):
        words = []
        for token in tokens:
            if token not in self.stop_words:
                flag = 0
                for c in token:
                    if ord(c) > ord('z'):
                        flag = 1
                if flag == 0:
                    words.append(token)
        # tokens = [token for token in tokens if not token in self.stop_words and ord(str(token[0])) <= ord('z')]
        return words

    def stem(self, tokens):
        stemmedTokens = [self.sno.stem(token) for token in tokens]
        return stemmedTokens


    def lemmatize(self, tokens):
        lemmatizer = WordNetLemmatizer()
        lemmatizedTokens = [lemmatizer.lemmatize(token) for token in tokens]
        return lemmatizedTokens
