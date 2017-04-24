import math
import nltk
import argparse



class unigramWordsList(object):
    """List of words dictionary and methods to add to them"""
    distinctWords = {}

    def __init__(self):
        self.distinctWords = {}

    def add_word(self, word):
        try:
            self.distinctWords[word] += 1
        except:
            self.distinctWords[word] = 1
    
    def get_number_of_distinct(self):
        return len(self.distinctWords)

    def printDistinctWords(self, fileHandle):
        for v in sorted(self.distinctWords.items(), key= lambda x : (-x[1], x[0])):
            fileHandle.write(str(v[0]) + " " + str(v[1]) + "\n")

    def printDistinctWordsConsole(self):
        for v in sorted(self.distinctWords.items(), key= lambda x : (-x[1], x[0])):
           print(str(v[0]) + " " + str(v[1]) + "\n")

    def getTotal(self):
        total = 0
        for value in self.distinctWords:
            if not (value == "\s" or value == "/s"):
                total += self.distinctWords[value]

        return total

    def get_N(self):
        total = 0
        for value in self.distinctWords:
            if not (value == "\s"):
                total += self.distinctWords[value]

        return total

    def printProbabilities(self):
        for v in sorted(self.distinctWords.items(), key= lambda x : (-x[1], x[0])):
            prob = v[1] / float(self.get_N())
            print str(v[0]) + " -> " + str(v[1]) + " [" + str(math.log(prob)) + "]"

    def get_V(self):
        return self.get_number_of_distinct() - 1



class bigramWordsList(object):
    """Dictionary of words along with their successors and the counts of each successor"""
    bigramWords = {}

    def __init__(self):
        self.bigramWords = {}

    def addBigram(self, bigram):
        if bigram[0] not in self.bigramWords:
            self.bigramWords[bigram[0]] = {}
            self.bigramWords[bigram[0]][bigram[1]] = 1
        else:
            if bigram[1] not in self.bigramWords[bigram[0]]:
                self.bigramWords[bigram[0]][bigram[1]] = 1
            else:
                self.bigramWords[bigram[0]][bigram[1]] += 1

    def getNumberOfDistinct(self):
        count = 0
        for key, value in self.bigramWords.iteritems():
            for key1, value1 in value.iteritems():
                count += 1
        return count

    #not working
    def printDistinctWords(self, fileHandle):
        for v in sorted(self.bigramWords.items(), key= lambda x : (-x[1], x[0])):
            fileHandle.write(str(v[0]) + " " + str(v[1]) + "\n")

    def getTotal(self):
        total = 0
        for value in self.bigramWords:
            total += self.bigramWords[value]

        return total

    def iteritems(self):
        return self.bigramWords.iteritems()

    def printBigrams(self):
        for key, value in self.bigramWords.iteritems():
            print "\n \nKEY: ",key
            for key1, value1 in value.iteritems():
                print("{0} : {1}".format(key1, value1))

    def print_probabilities(self):
        for key in self.bigramWords.items():
            count = sum(self.bigramWords[key].values())
            for key1 in self.bigramWords[key].items():
                prob = self.bigramWords[key][key1] / float(count)
                print str(key) + " " + str(key1) + " -> " + str(self.bigramWords[key][key1]) + " [" + str(math.log(prob)) + "]"

    def calculateSuccessorCounts(self, pairs):
        count = 0
        for val in pairs.itervalues():
            if isinstance(val, ):
                print val[1]
                count += val[1]
        return count

class bigram(object):
    pass

sentences = 0
unigramWordsObj = unigramWordsList()
bigramWordsObj = bigramWordsList()


parser = argparse.ArgumentParser(description="set training, test, and output files")
parser.add_argument('train', help='name of train file')
parser.add_argument('test', help='name out test file')
parser.add_argument('output', help='name of output file')

args = parser.parse_args()

with open(args.train) as fileContents:
    fileText = fileContents.read()

    fileTextLineSplit = fileText.split('\n')

    mergedFileText = ' '.join(fileTextLineSplit)

    for sentence in nltk.sent_tokenize(mergedFileText):
        sentence = ' \s ' + sentence + ' /s '
        #print(sentence)
        sentences += 1

        for word in nltk.word_tokenize(sentence):
            print(word)
            unigramWordsObj.add_word(word)

        bigrams = nltk.bigrams(nltk.word_tokenize(sentence))
        for bigram in bigrams:
            #print bigram
            bigramWordsObj.addBigram(bigram)

    #bigramWordsObj.printBigrams()
    print ("================================\n")
    #unigramWordsObj.printDistinctWordsConsole()

    unigramWordsObj.printProbabilities()

    print ("\n")

    bigramWordsObj.print_probabilities()

with open(args.output, 'w') as outFile:
    outFile.write("Total # of sentences: " + str(sentences) + '\n')
    outFile.write("Total # of tokens: " + str(unigramWordsObj.getTotal()) + '\n')
    outFile.write("# of unique bigrams " + str(bigramWordsObj.getNumberOfDistinct()) + '\n')
    outFile.write("=> _N " + str(unigramWordsObj.get_N()) + ", _V " + str(unigramWordsObj.get_V()))
    outFile.write("\n")
    outFile.write("================================\n")

    unigramWordsObj.printDistinctWords(outFile)



