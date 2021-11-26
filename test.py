from flask import wrappers
from flask.globals import session
import numpy as np
import time
import math
import random
import os
from PyDictionary import PyDictionary

class testWrapper():
    def __init__(self):
        self.tests = {}
        self.allWords = self.importWords()

    def importWords(self):
        a1 = np.genfromtxt(os.getcwd()+"/words/a1.txt", dtype=str,
                       encoding='UTF-8', delimiter="\n")
        a2 = np.genfromtxt(os.getcwd()+"/words/a2.txt", dtype=str,
                         encoding='UTF-8', delimiter="\n")
        b1 = np.genfromtxt(os.getcwd()+"/words/b1.txt", dtype=str,
                         encoding='UTF-8', delimiter="\n")
        b2 = np.genfromtxt(os.getcwd()+"/words/b2.txt", dtype=str,
                         encoding='UTF-8', delimiter="\n")
        c1 = np.genfromtxt(os.getcwd()+"/words/c1.txt", dtype=str,
                         encoding='UTF-8', delimiter="\n")
        c2 = np.genfromtxt(os.getcwd()+"/words/c2.txt", dtype=str,
                         encoding='UTF-8', delimiter="\n")
        allWords = (a1, a2, b1, b2, c1, c2)
        return allWords

    def createTest(self, session):
        self.tests[session] = Test(self.allWords)
    

def testTest():
    wrapper = testWrapper()
    wrapper.createTest("111")
    a = wrapper.tests["111"]
    wrapper.createTest("222")
    b = wrapper.tests["222"]
    wrapper.createTest("333")
    c = wrapper.tests["333"]

    print(wrapper.tests)
    

    for i in range (5):
        word = a.getWord()
        print(word)
        a.setAnswer(int(input()))
    print(a.levels[a.currentCall])

    for i in range (5):
        word = b.getWord()
        print(word)
        b.setAnswer(int(input()))
    print(b.levels[b.currentCall])

    for i in range (5):
        word = c.getWord()
        print(word)
        c.setAnswer(int(input()))
    print(c.levels[c.currentCall])

    print(a.levels[a.currentCall])
    print(b.levels[b.currentCall])
    print(c.levels[c.currentCall])
    # print(a.currentCatv)
    # print(a.levels)
    # print(a.itemsAndResponses)

class Test:
    def __init__(self, allWords, initialLevel=3):
        self.allWords = allWords
        self.levels = np.empty(1)
        self.levels[0] = initialLevel
        self.itemsAndResponses = np.empty([0, 2])
        self.currentCall = 0
        self.possibleLevels = np.array([1, 2, 3, 4, 5, 6])
        self.currentCatv = np.empty([1, 6])
    
        
    def getWord(self):
        ##todo: check to not repeat
        wordNumber = random.randrange(0, len(self.allWords[int(self.levels[self.currentCall]-1)]))
        outputWord = self.allWords[int(self.levels[self.currentCall]-1)][wordNumber]
        return outputWord

    def setAnswer(self, ans):
        ##todo: check to accept only boolean
        item = self.levels[self.currentCall]
        self.itemsAndResponses = np.append(self.itemsAndResponses, [[item, ans]], axis=0)
        self.currentCatv = self.catvalues(self.itemsAndResponses, self.possibleLevels)
        currentLevel = np.argmax(self.currentCatv)+1
        self.levels = np.append(self.levels, currentLevel)
        self.currentCall += 1
        
    def runTest(self, iterationsNumber = 20, initialLevel = 3):
        currentLevel = np.empty(iterationsNumber+1, dtype=int)
        currentLevel[0] = initialLevel
        temp = -1
        itemsAndResponses = np.empty([0, 2])
        for i in range(iterationsNumber):
            print("Do you know this word? (1/0)")
            wordNumber = random.randrange(0, len(self.allWords[currentLevel[i]-1]))
            while temp == wordNumber: ##to avoid repeating words
                wordNumber = random.randrange(0, len(self.allWords[currentLevel[i]-1]))
            print(self.allWords[currentLevel[i]-1][wordNumber])
            item = currentLevel[i]
            response = int(input())
            itemsAndResponses = np.append(itemsAndResponses, [[item, response]], axis=0)
            levels = np.array([1, 2, 3, 4, 5, 6])
            catv = self.catvalues(itemsAndResponses, levels)
            currentLevel[i+1] = np.argmax(catv)+1
            temp = wordNumber
        return currentLevel, catv, itemsAndResponses

    def rasch(self, cefr, level):
        return 1/(1+math.exp(cefr-level))

    def cat(self, items, lev):
        probarray = np.empty(len(items))
        for i in range(len(items)):
            prob = ((self.rasch(items[i, 0], lev)**items[i, 1]))*((1-self.rasch(items[i, 0], lev))**(1-items[i, 1]))
            if i > 0:
                prob = prob*probarray[i-1]                                               
            probarray[i] = prob
        return math.log10(probarray[i])

    def catvalues(self, items, levs):
        values = np.empty(len(levs))
        for i in range(len(levs)):
            values[i] = self.cat(items, i+1)
        return values

    def clear(self):
        self.levels = np.empty(1)
        self.levels[0] = 3
        self.itemsAndResponses = np.empty([0, 2])
        self.currentCall = 0
        self.possibleLevels = np.array([1, 2, 3, 4, 5, 6])
        self.currentCatv = np.empty([1, 6])        


# if __name__ == '__main__':
#    testTest()

