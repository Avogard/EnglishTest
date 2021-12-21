from flask import wrappers
from flask.globals import session
import numpy as np
import time
import math
import random
import os
from PyDictionary import PyDictionary

# class testWrapper():
#     def __init__(self):
#         self.tests = {}
#         self.allWords = self.importWords()

#     def importWords(self):
#         a1 = np.genfromtxt(os.getcwd()+"/words/a1.txt", dtype=str,
#                          encoding='UTF-8', delimiter="\n")
#         a2 = np.genfromtxt(os.getcwd()+"/words/a2.txt", dtype=str,
#                          encoding='UTF-8', delimiter="\n")
#         b1 = np.genfromtxt(os.getcwd()+"/words/b1.txt", dtype=str,
#                          encoding='UTF-8', delimiter="\n")
#         b2 = np.genfromtxt(os.getcwd()+"/words/b2.txt", dtype=str,
#                          encoding='UTF-8', delimiter="\n")
#         c1 = np.genfromtxt(os.getcwd()+"/words/c1.txt", dtype=str,
#                          encoding='UTF-8', delimiter="\n")
#         c2 = np.genfromtxt(os.getcwd()+"/words/c2.txt", dtype=str,
#                          encoding='UTF-8', delimiter="\n")
#         allWords = (a1, a2, b1, b2, c1, c2)
#         return allWords

#     def createTest(self, session):
#         self.tests[session] = Test(self.allWords)
    

def testTest():
    mytest = Test()
    # for _ in range(2):
    #     print(mytest.getWord())
    #     mytest.setAnswer(int(input()))

    dic = {
        "cucumber": 1,
        "incise": 0,
        "hook": 1,
        "theoretical": 1,
        "quince": 0,
        "refract": 0,
        "merchantman": 1,
        "stance": 1,
        "coot": 0,
        "practitioner": 1,
    }

    mytest.setAnswers(dic)
    print(mytest.currentCatv)
    print("")
    print(mytest.levels)
    print("")
    print(mytest.itemsAndResponses)
    print("")
    print(mytest.usedWords)

class Test:
    # def __init__(self, allWords, initialLevel=3):
    def __init__(self, initialLevel=3):
        self.allWords = self.importWords()
        self.levels = np.empty(1)
        self.levels[0] = initialLevel
        self.itemsAndResponses = np.empty([0, 2])
        self.currentCall = 0
        self.possibleLevels = np.array([1, 2, 3, 4, 5, 6])
        self.currentCatv = np.empty([1, 6])
        self.usedWords = []
    
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
        
    def getWord(self):
        wordNumber = random.randrange(0, len(self.allWords[int(self.levels[self.currentCall]-1)]))
        outputWord = self.allWords[int(self.levels[self.currentCall]-1)][wordNumber]
        while outputWord in self.usedWords: #no repeats
            wordNumber = random.randrange(0, len(self.allWords[int(self.levels[self.currentCall]-1)]))
            outputWord = self.allWords[int(self.levels[self.currentCall]-1)][wordNumber]
        self.usedWords.append(outputWord)
        return outputWord

    def setAnswer(self, ans):
        item = self.levels[self.currentCall]
        self.itemsAndResponses = np.append(self.itemsAndResponses, [[item, ans]], axis=0)
        self.currentCatv = self.catvalues(self.itemsAndResponses, self.possibleLevels)
        currentLevel = np.argmax(self.currentCatv)+1
        self.levels = np.append(self.levels, currentLevel)
        self.currentCall += 1

    # accepts list of dictionaries of answers
    # [{"word1": 1}, {"word2": 1} {"word3": 0} ...]
    def setAnswers(self, answers): 
        for dict in answers:
            [(word, ans)] = dict.items()
            item = self.levels[self.currentCall]
            self.itemsAndResponses = np.append(self.itemsAndResponses, [[item, ans]], axis=0)
            self.currentCatv = self.catvalues(self.itemsAndResponses, self.possibleLevels)
            currentLevel = np.argmax(self.currentCatv)+1
            self.levels = np.append(self.levels, currentLevel)
            self.currentCall += 1
            self.usedWords.append(word)
        
    # def runTest(self, iterationsNumber = 20, initialLevel = 3):
    #     currentLevel = np.empty(iterationsNumber+1, dtype=int)
    #     currentLevel[0] = initialLevel
    #     temp = -1
    #     itemsAndResponses = np.empty([0, 2])
    #     for i in range(iterationsNumber):
    #         print("Do you know this word? (1/0)")
    #         wordNumber = random.randrange(0, len(self.allWords[currentLevel[i]-1]))
    #         while temp == wordNumber: ##to avoid repeating words
    #             wordNumber = random.randrange(0, len(self.allWords[currentLevel[i]-1]))
    #         print(self.allWords[currentLevel[i]-1][wordNumber])
    #         item = currentLevel[i]
    #         response = int(input())
    #         itemsAndResponses = np.append(itemsAndResponses, [[item, response]], axis=0)
    #         levels = np.array([1, 2, 3, 4, 5, 6])
    #         catv = self.catvalues(itemsAndResponses, levels)
    #         currentLevel[i+1] = np.argmax(catv)+1
    #         temp = wordNumber
    #     return currentLevel, catv, itemsAndResponses


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


if __name__ == '__main__':
   testTest()

