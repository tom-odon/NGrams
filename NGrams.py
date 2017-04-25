#Thomas Odon DPUID 0956600
#CSC 594
#HW #2
import math
import nltk
import argparse
import io


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
        for v in sorted(self.distinctWords.iteritems()):
            if isinstance(v[1], int):
                fileHandle.write(str(v[0]) + " " + str(v[1]) + "\n")
            elif isinstance(v[1], tuple):
                fileHandle.write(str(v[0]) + " " + str(v[1][0]) + " -> " + "[" +str(v[1][1]) + "]" + "\n")

    def printDistinctWordsConsole(self):
        for v in sorted(self.distinctWords.items(), key= lambda x : (-x[1], x[0])):
           print(str(v[0]) + " " + str(v[1]) + "\n")

    def getTotal(self):
        total = 0
        for v in self.distinctWords.items():
            if not (v[0] == "\s" or v[0] == "/s"):
                if isinstance(v[1], int):
                    total += v[1]
                elif isinstance(v[1], tuple):
                    total += v[1][0]
        return total

    def get_N(self):
        total = 0
        for v in self.distinctWords.items():
            if not (v[0] == "\s"):
                if isinstance(v[1], int):
                    total += v[1]
                elif isinstance(v[1], tuple):
                    total += v[1][0]
        return total

    def printProbabilities(self):
        for key, value in self.distinctWords.items():
            print("{0} -> {1} [{2}]".format(key, value[0], value[1]))

    def set_probabilities(self):
        _n = float(self.getTotal())
        for key, value in sorted(self.distinctWords.items()):
            prob = math.log(value / _n )
            self.distinctWords[key] = value, prob


    def get_V(self):
        return self.get_number_of_distinct() - 1

    def get_unigram_probability(self, word):
        probability = self.distinctWords.get(word)
        if probability is None:
            return 0
        #print probability
        return probability[1]



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
            for key1, value1 in value.iteritems():
                print("{0} {1} -> {2} [{3}]".format(key, key1, value1[0], value1[1]))


    def set_probabilities(self):
        for key, value in self.bigramWords.items():
            count = 0
            for key1, value1 in value.iteritems():
                count += value1
            for key1, value1 in value.iteritems():
                prob = value1 / float(count)
                self.bigramWords[key][key1] = value1, math.log(prob)

    def get_bigram_probability(self, bigram):
        probability1 = self.bigramWords.get(bigram[0])
        if probability1 is None:
            return 0
        probability2 = probability1.get(bigram[1])
        if probability2 is None:
            return 0
        return probability2[1]


train_sentences = 0
test_sentences = 0
unigramWordsObj = unigramWordsList()
bigramWordsObj = bigramWordsList()
unigramWordsObjTest = unigramWordsList()
bigramWordsObjTest = bigramWordsList()


parser = argparse.ArgumentParser(description="set training, test, and output files")
parser.add_argument('train', help='name of train file')
parser.add_argument('test', help='name out test file')
parser.add_argument('output', help='name of output file')

args = parser.parse_args()
fileText = ""
encodings = ['utf-8', 'windows-1250', 'windows-1252', 'latin-1']
for e in encodings:
    try:
        print e
        with io.open(args.train, 'r', encoding=e) as fileContents:
            fileText = fileContents.read()
            fileTextLineSplit = fileText.split('\n')

            mergedFileText = ' '.join(fileTextLineSplit)

            for sentence in nltk.sent_tokenize(mergedFileText):
                sentence = ' \s ' + sentence + ' /s '
                # print(sentence)
                train_sentences += 1

                for word in nltk.word_tokenize(sentence):
                    # print(word)
                    unigramWordsObj.add_word(word)

                bigrams = nltk.bigrams(nltk.word_tokenize(sentence))
                for bigram in bigrams:
                    # print bigram
                    bigramWordsObj.addBigram(bigram)

            # bigramWordsObj.printBigrams()
            # unigramWordsObj.printDistinctWordsConsole()

            unigramWordsObj.set_probabilities()
            # unigramWordsObj.printProbabilities()

            print ("\n")

            bigramWordsObj.set_probabilities()
            # bigramWordsObj.printBigrams()
    except UnicodeDecodeError:
        print('got unicode error with %s , trying different encoding' % e)
    else:
        print('opening the file with encoding:  %s ' % e)
        break

for e in encodings:
    try:
        print e
        with io.open(args.test, 'r', encoding=e) as fileContents, open(args.output, 'w') as outFile:
            fileText = fileContents.read()

            fileTextLineSplit = fileText.split('\n')

            mergedFileText = ' '.join(fileTextLineSplit)

            for sentence in nltk.sent_tokenize(mergedFileText):
                log_probability_unigram = 0
                log_probability_bigram = 0
                print "Sentence ", (test_sentences + 1), ": ", sentence, "\n"
                outFile.write("Sentence " + str(test_sentences + 1) + ": " + sentence + "\n")
                sentence = ' \s ' + sentence + ' /s '
                test_sentences += 1

                for word in nltk.word_tokenize(sentence):
                    # print(word)
                    unigramWordsObjTest.add_word(word)
                    log_probability_unigram += unigramWordsObj.get_unigram_probability(word)

                bigramsTest = nltk.bigrams(nltk.word_tokenize(sentence))
                for bigram in bigramsTest:
                    bigramWordsObjTest.addBigram(bigram)
                    log_probability_bigram += bigramWordsObj.get_bigram_probability(bigram)

                # bigramWordsObjTest.printBigrams()

                outFile.write("- unigram [Prob] " + str(math.exp(log_probability_unigram)) +"\n")
                outFile.write("- bigram  [Prob] " + str(math.exp(log_probability_bigram))+"\n")

            outFile.write("\nTraining Data: +\n")
            outFile.write("Total # of sentences: " + str(train_sentences) + '\n')
            outFile.write("Total # of tokens: " + str(unigramWordsObj.getTotal()) + '\n')
            outFile.write("# of unique bigrams " + str(bigramWordsObj.getNumberOfDistinct()) + '\n')
            outFile.write("=> _N " + str(unigramWordsObj.get_N()) + ", _V " + str(unigramWordsObj.get_V()))
            outFile.write("\n")
            outFile.write("================================\n")
            outFile.write("\nTest Data: +\n")
            outFile.write("Total # of sentences: " + str(test_sentences) + '\n')
            outFile.write("Total # of tokens: " + str(unigramWordsObjTest.getTotal()) + '\n')
            outFile.write("# of unique bigrams " + str(bigramWordsObjTest.getNumberOfDistinct()) + '\n')
            outFile.write("=> _N " + str(unigramWordsObjTest.get_N()) + ", _V " + str(unigramWordsObjTest.get_V()))
            outFile.write("\n")
    except UnicodeDecodeError:
        print('got unicode error with %s , trying different encoding' % e)
    else:
        print('opening the file with encoding:  %s ' % e)
        break



