import sys
import re
import math

class NBClassify:
    dicOfInstancesWithLabels = {}
    posPrior = 0
    negPrior = 0
    truthPrior = 0
    decepPrior = 0

    def readNbModelFile(self):
        count = 1
        with open("nbmodel.txt", "r") as file:
            for line in file:
                line = line.strip(' ')
                line = line.strip('\n')
                if count <=4:
                    priorProb = line.split(' ')
                    if count == 1:
                        self.posPrior = float(priorProb[4])
                    if count == 2:
                        self.negPrior = float(priorProb[4])
                    if count == 3:
                        self.truthPrior = float(priorProb[4])
                    if count == 4:
                        self.decepPrior = float(priorProb[4])
                else:
                    line = file.readline()
                    line = line.strip(' ')
                    line = line.strip('\n')
                    if line == "":
                        continue
                    word = line
                    line = file.readline()
                    line = file.readline()
                    line = line.strip(' ')
                    line = line.strip('\n')
                    wordProb = line.split(' ')
                    wordPosProb = float(wordProb[3])
                    line = file.readline()
                    line = line.strip(' ')
                    line = line.strip('\n')
                    wordProb = line.split(' ')
                    wordNegProb = float(wordProb[3])
                    line = file.readline()
                    line = line.strip(' ')
                    line = line.strip('\n')
                    wordProb = line.split(' ')
                    wordTruthProb = float(wordProb[3])
                    line = file.readline()
                    line = line.strip(' ')
                    line = line.strip('\n')
                    wordProb = line.split(' ')
                    wordDecepProb = float(wordProb[3])
                    self.dicOfInstancesWithLabels[word] = {"positive": wordPosProb, "negative": wordNegProb,
                                                           "truthful": wordTruthProb, "deceptive": wordDecepProb}
                    #line = file.readline()
                count += 1
        #print(self.dicOfInstancesWithLabels)


    def readDvlpmntFile(self, filename):
        stopwords = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
                     "aren't", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both",
                     "but", "by", "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't",
                     "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had", "hadn't",
                     "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
                     "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm",
                     "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more"
                     , "mustn't", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or",
                     "ought", "our", "ours    ourselves", "out", "over", "own", "same", "shan't", "she",
                     "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's",
                     "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they",
                     "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under",
                     "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't",
                     "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom",
                     "why", "why's", "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've",
                     "your", "yours", "yourself", "yourselves", 'a', 'about', 'above', 'across', 'after', 'again',
                     'against', 'all', 'almost', 'alone', 'btw', 'north', 'south', 'east', 'west', 'sarita', 'woke', 'wake',
                     'suv', 'omg', 'asap', 'contain', 'au', 'demi', 'mam', 'sir', "ma'am", "i'm'", 'ohh', 'oh', 'duh',
                     'go', 'goes', 'went', 'gone', 'dollar', 'dollars', 'cents', 'cent', 'usa', 'dont', 'aaa',
                     'along', 'already', 'also', 'although', 'always', 'among', 'an', 'and', 'another', 'any',
                     'anybody', 'anyone', 'anything', 'anywhere', 'are', 'area', 'areas', 'around', 'as', 'ask',
                     'asked', 'asking', 'asks', 'at', 'away', 'b', 'back', 'backed', 'backing', 'backs', 'be',
                     'became', 'because', 'become', 'becomes', 'been', 'before', 'began', 'behind', 'being',
                     'beings', 'between', 'both', 'but', 'by', 'c', 'came', 'can', 'cannot', 'couldnt',
                     'case', 'cases', 'certain', 'certainly', 'clear', 'clearly', 'come', 'could', 'coz', 'd', 'did',
                     'differ', 'different', 'differently', 'do', 'does', 'done', 'down', 'downed', 'downing', 'downs',
                     'during', 'e', 'each', 'early', 'either', 'end', 'ended', 'ending', 'ends', 'enough', 'even',
                     'evenly', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'f',
                     'faces', 'fact', 'facts', 'far', 'felt', 'few', 'find', 'first', 'for', 'four', 'from',
                     'full', 'fully', 'further', 'furthered', 'furthering', 'furthers', 'g', 'gave', 'general',
                     'generally', 'get', 'gets', 'give', 'given', 'gives', 'go', 'going', 'goods', 'got',
                     'group', 'grouped', 'grouping', 'groups', 'h', 'had', 'has',
                     'have', 'having', 'he', 'her', 'here', 'herself',
                     'him', 'himself', 'his', 'how', 'however', 'i', 'if', 'important', 'in', 'into', 'is', 'it', 'its',
                     'itself', 'j', 'just', 'k', 'keep', 'keeps',
                     'knew', 'know', 'known', 'knows', 'l', 'largely', 'later', 'latest',
                     'least', 'let', 'lets', 'likely', 'm', 'made', 'make',
                     'making', 'man', 'many', 'may', 'me', 'member', 'members', 'men', 'might', 'more', 'most',
                     'mostly', 'mr', 'mrs', 'much', 'must', 'my', 'myself', 'n', 'necessary', 'need', 'needed',
                     'needing', 'needs', 'new', 'next',
                     'noone', 'nothing', 'now', 'nowhere', 'number', 'numbers', 'o', 'of', 'off', 'often',
                     'old', 'older', 'oldest', 'on', 'once', 'one', 'only', 'open', 'opened', 'opening', 'opens', 'or',
                     'order', 'ordered', 'ordering', 'orders', 'other', 'others', 'our', 'out', 'over', 'p', 'part',
                     'parted', 'parting', 'parts', 'per', 'perhaps', 'place', 'places', 'point', 'pointed', 'pointing',
                     'points', 'possible', 'present', 'presented', 'presenting', 'presents',
                     'put', 'puts', 'q', 'quite', 'r', 'rather', 'really', 'right', 'room', 'rooms', 's',
                     'said', 'same', 'saw', 'say', 'says', 'second', 'seconds', 'see', 'seem', 'seemed', 'seeming',
                     'seems', 'sees', 'several', 'shall', 'she', 'should', 'show', 'showed', 'showing', 'shows', 'side',
                     'sides', 'since', 'so', 'some', 'somebody', 'someone', 'something',
                     'somewhere', 'state', 'states', 'still', 'such', 'sure', 't', 'take', 'taken', 'than',
                     'that', 'the', 'their', 'them', 'then', 'there', 'therefore', 'these', 'they', 'thing', 'things',
                     'think', 'thinks', 'this', 'those', 'though', 'thought', 'thoughts', 'three', 'through', 'thus',
                     'to', 'today', 'together', 'too', 'took', 'toward', 'turn', 'turned', 'turning', 'turns', 'two',
                     'u', 'under', 'until', 'up', 'upon', 'us', 'use', 'used', 'uses', 'v', 'very', 'w', 'want',
                     'wanted', 'wanting', 'wants', 'was', 'way', 'ways', 'we', 'well', 'wells', 'went', 'were', 'what',
                     'when', 'where', 'whether', 'which', 'while', 'who', 'whole', 'whose', 'why', 'will', 'with',
                     'within', 'without', 'work', 'worked', 'working', 'works', 'would', 'x', 'y', 'year', 'years',
                     'yet', 'you', 'young', 'younger', 'youngest', 'your', 'yours', 'z']


        outputList = []

        #with open("train-dev.txt", "r") as file:
        with open(filename, "r") as file:
            for line in file:
                splitID = line.split(' ',1)
                reviewID = splitID[0]
                reviewStr = splitID[1]
                reviewStr = reviewStr.lower()
                reviewStr = re.sub("[^'A-z -]", '', reviewStr)
                reviewWordsList = reviewStr.split(' ')

                for word in reviewWordsList:
                    word = word.strip(" ")
                    if len(word) <= 2:
                        reviewWordsList.remove(word)

                setOfStopWords = set(reviewWordsList) & set(stopwords)
                for word in setOfStopWords:
                    reviewWordsList = [x for x in reviewWordsList if x != word]

                for word in reviewWordsList:
                    if "'" in word:
                        reviewWordsList.remove(word)
                        aposIndex = word.index("'")
                        word = word[0:aposIndex]
                        reviewWordsList.append(word)


                setOfStopWords = set(reviewWordsList) & set(stopwords)
                for word in setOfStopWords:
                    reviewWordsList = [x for x in reviewWordsList if x != word]

                if '' in reviewWordsList:
                    reviewWordsList = [x for x in reviewWordsList if x != '']

                #print(reviewID)
                #print(reviewWordsList)

                listForID = [reviewID]
                truthfulProb = self.calculateProbability(reviewWordsList, "truthful")
                deceptiveProb = self.calculateProbability(reviewWordsList, "deceptive")
                if truthfulProb >= deceptiveProb:
                    listForID.append("truthful")
                else:
                    listForID.append("deceptive")
                positiveProb = self.calculateProbability(reviewWordsList, "positive")
                negativeProb = self.calculateProbability(reviewWordsList, "negative")
                if positiveProb >= negativeProb:
                    listForID.append("positive")
                else:
                    listForID.append("negative")

                outputList.append(listForID)
        #print(outputList)
        self.printOutputFile(outputList)


    def calculateProbability(self, reviewWordsList, label):
         probValue = 1
         #learnObject = nblearn3.NBLearn()
         prior = 0;
         if label == "positive":
             prior = self.posPrior
         if label == "negative":
             prior = self.negPrior
         if label == "truthful":
             prior = self.truthPrior
         if label == "deceptive":
             prior = self.decepPrior
         probValue += prior


         for word in reviewWordsList:
             if word in self.dicOfInstancesWithLabels:
                 probValue += self.dicOfInstancesWithLabels[word][label]
         return probValue


    def printOutputFile(self, outputList):
        nbOutputFile = open("nboutput.txt", 'w')
        for innerList in outputList:
            nbOutputFile.write(innerList[0] + " " + innerList[1] + " " + innerList[2] + "\n")
        nbOutputFile.close()


classifyObj = NBClassify()
classifyObj.readNbModelFile()
classifyObj.readDvlpmntFile(sys.argv[1])
