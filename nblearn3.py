import sys
import re
import math

class NBLearn:
    dicOfLabels = {}
    dicOfInstancesWithLabels = {}
    countOfPos = 0
    countOfNeg = 0
    countOfTruth = 0
    countOfDecep = 0
    posPrior = 0
    negPrior = 0
    truthPrior = 0
    decepPrior = 0

    totalPosWordsAfterSmoothing = 0
    totalNegWordsAfterSmoothing = 0
    totalTruthWordsAfterSmoothing = 0
    totalDecepWordsAfterSmoothing = 0

    def readTrainText(self, trainingFile):
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


        #with open("test.txt", "r") as file:
        #with open("train-text.txt", "r") as file:
        #print(trainingFile)
        with open(trainingFile, "r") as file:
            for line in file:
                line = line.replace("-", " ")
                splitID = line.split(' ',1)
                reviewID = splitID[0]
                reviewStr = splitID[1]
                reviewStr = reviewStr.lower()
                reviewStr = re.sub("[^'A-z ]", ' ', reviewStr)
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
                self.createDictOfInstances(reviewID, reviewWordsList)
            #print(self.dicOfInstancesWithLabels)


    def readTrainLabels(self, labelFile):
        #with open("train-labels.txt", "r") as file:
        #print(labelFile)
        with open(labelFile, "r") as labelfile:
            for line in labelfile:
                #print(line)
                line = line.strip(' ')
                line = line.strip('\n')
                splitLabels = line.split(' ')
                reviewID = splitLabels[0]
                truthDecepLabel = splitLabels[1]
                posNegLabel = splitLabels[2]
                self.dicOfLabels[reviewID] = [posNegLabel, truthDecepLabel]
        #print(self.dicOfLabels)


    def createDictOfInstances(self, reviewID, reviewWordsList):
        labelsForID = self.dicOfLabels[reviewID]
        #print(labelsForID)
        posNegLabel = labelsForID[0]
        truthDecepLabel = labelsForID[1]

        if posNegLabel == "positive":
            self.countOfPos += 1
            appendStr = "positive"
            appendInvStr = "negative"
            for word in reviewWordsList:
                if word not in self.dicOfInstancesWithLabels:
                    self.dicOfInstancesWithLabels[word] = {"positive": 0, "negative": 0, "truthful": 0, "deceptive": 0}
                self.assignLabelAndCreateDictionary(word, appendStr, appendInvStr)

        if posNegLabel == "negative":
            self.countOfNeg += 1
            appendStr = "negative"
            appendInvStr = "positive"
            for word in reviewWordsList:
                if word not in self.dicOfInstancesWithLabels:
                    self.dicOfInstancesWithLabels[word] = {"positive": 0, "negative": 0, "truthful": 0, "deceptive": 0}
                self.assignLabelAndCreateDictionary(word, appendStr, appendInvStr)

        if truthDecepLabel == "truthful":
            self.countOfTruth += 1
            appendStr = "truthful"
            appendInvStr = "deceptive"
            for word in reviewWordsList:
                if word not in self.dicOfInstancesWithLabels:
                    self.dicOfInstancesWithLabels[word] = {"positive": 0, "negative": 0, "truthful": 0, "deceptive": 0}
                self.assignLabelAndCreateDictionary(word, appendStr, appendInvStr)

        if truthDecepLabel == "deceptive":
            self.countOfDecep += 1
            appendStr = "deceptive"
            appendInvStr = "truthful"
            for word in reviewWordsList:
                if word not in self.dicOfInstancesWithLabels:
                    self.dicOfInstancesWithLabels[word] = {"positive": 0, "negative": 0, "truthful": 0, "deceptive": 0}
                self.assignLabelAndCreateDictionary(word, appendStr, appendInvStr)



    def assignLabelAndCreateDictionary(self, word, label, invLabel):
        self.dicOfInstancesWithLabels[word][label] += 1



    def printDictionary(self):
        for key in self.dicOfInstancesWithLabels:
            print(key + " : ")
            print(self.dicOfInstancesWithLabels[key])
            #print("\n")
        print(len(self.dicOfInstancesWithLabels))

    def calculatePriorProb(self):
        self.posPrior = math.log(self.countOfPos / (self.countOfPos+self.countOfNeg))
        self.negPrior = math.log(self.countOfNeg / (self.countOfPos + self.countOfNeg))
        self.truthPrior = math.log(self.countOfTruth / (self.countOfTruth + self.countOfDecep))
        self.decepPrior = math.log(self.countOfDecep / (self.countOfTruth + self.countOfDecep))

        #print(posPrior, negPrior, truthPrior, decepPrior)


    def addOneSmoothing(self):
        numOfPosWords = 0
        numOfNegWords = 0
        numOfTruthWords = 0
        numOfDecepWords = 0
        for instance in self.dicOfInstancesWithLabels:
            numBeforeSmoothing = self.dicOfInstancesWithLabels[instance]["positive"]
            numOfPosWords += numBeforeSmoothing
            numAfterSmoothing = numBeforeSmoothing + 1
            self.totalPosWordsAfterSmoothing += numAfterSmoothing
            self.dicOfInstancesWithLabels[instance]["positive"] = numAfterSmoothing

            numBeforeSmoothing = self.dicOfInstancesWithLabels[instance]["negative"]
            numOfNegWords += numBeforeSmoothing
            numAfterSmoothing = numBeforeSmoothing + 1
            self.totalNegWordsAfterSmoothing += numAfterSmoothing
            self.dicOfInstancesWithLabels[instance]["negative"] = numAfterSmoothing

            numBeforeSmoothing = self.dicOfInstancesWithLabels[instance]["truthful"]
            numOfTruthWords += numBeforeSmoothing
            numAfterSmoothing = numBeforeSmoothing + 1
            self.totalTruthWordsAfterSmoothing += numAfterSmoothing
            self.dicOfInstancesWithLabels[instance]["truthful"] = numAfterSmoothing

            numBeforeSmoothing = self.dicOfInstancesWithLabels[instance]["deceptive"]
            numOfDecepWords += numBeforeSmoothing
            numAfterSmoothing = numBeforeSmoothing + 1
            self.totalDecepWordsAfterSmoothing += numAfterSmoothing
            self.dicOfInstancesWithLabels[instance]["deceptive"] = numAfterSmoothing

        #print(numOfPosWords, self.totalPosWordsAfterSmoothing, self.totalPosWordsAfterSmoothing - numOfPosWords)
        #print(numOfNegWords, self.totalNegWordsAfterSmoothing, self.totalNegWordsAfterSmoothing - numOfNegWords)
        #print(numOfTruthWords, self.totalTruthWordsAfterSmoothing, self.totalTruthWordsAfterSmoothing - numOfTruthWords)
        #print(numOfDecepWords, self.totalDecepWordsAfterSmoothing, self.totalDecepWordsAfterSmoothing - numOfDecepWords)


    def printNBModel(self):
        base = 2
        nbModelFile = open("nbmodel.txt", 'w')
        nbModelFile.write("Prior Positive Probability : " + str(self.posPrior))
        nbModelFile.write("\n")
        nbModelFile.write("Prior Negative Probability : " + str(self.negPrior))
        nbModelFile.write("\n")
        nbModelFile.write("Prior Truthful Probability : " + str(self.truthPrior))
        nbModelFile.write("\n")
        nbModelFile.write("Prior Deceptive Probability : " + str(self.decepPrior))
        nbModelFile.write("\n")
        nbModelFile.write("\n")

        for instance in self.dicOfInstancesWithLabels:
            nbModelFile.write(instance)
            nbModelFile.write("\n")
            nbModelFile.write("No of Instances and Probabilities:")
            nbModelFile.write("\n")
            probOfPositive = math.log(
                self.dicOfInstancesWithLabels[instance]["positive"]/self.totalPosWordsAfterSmoothing)
            nbModelFile.write(
                "positive : " + str(self.dicOfInstancesWithLabels[instance]["positive"]) + " " + str(probOfPositive))
            nbModelFile.write("\n")
            probOfNegative = math.log(
                self.dicOfInstancesWithLabels[instance]["negative"] / self.totalNegWordsAfterSmoothing)
            nbModelFile.write(
                "negative : " + str(self.dicOfInstancesWithLabels[instance]["negative"]) + " " + str(probOfNegative))
            nbModelFile.write("\n")
            probOfTruthful = math.log(
                self.dicOfInstancesWithLabels[instance]["truthful"] / self.totalTruthWordsAfterSmoothing)
            nbModelFile.write(
                "truthful : " + str(self.dicOfInstancesWithLabels[instance]["truthful"]) + " " + str(probOfTruthful))
            nbModelFile.write("\n")
            probOfDeceptive = math.log(
                self.dicOfInstancesWithLabels[instance]["deceptive"] / self.totalDecepWordsAfterSmoothing)
            nbModelFile.write(
                "deceptive : " + str(self.dicOfInstancesWithLabels[instance]["deceptive"]) + " " + str(probOfDeceptive))
            nbModelFile.write("\n")
            nbModelFile.write("\n")
        nbModelFile.close()



learnObject = NBLearn()
learnObject.readTrainLabels(sys.argv[2])
learnObject.readTrainText(sys.argv[1])
# learnObject.readTrainLabels("train-labels.txt")
# learnObject.readTrainText("train-text.txt")
learnObject.calculatePriorProb()
learnObject.addOneSmoothing()
#learnObject.printDictionary()
learnObject.printNBModel()








