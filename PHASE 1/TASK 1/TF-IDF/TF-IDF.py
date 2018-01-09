import os
from math import log
import traceback


INPUT_DIRECTORY = "CORPUS"
INPUT_FOLDER = os.getcwd() + "/" + INPUT_DIRECTORY
N = len(os.listdir(INPUT_FOLDER))
TF_IDF_SCORE_LIST = "TF_IDF_SCORE_LIST.txt"
QUERY_FILE = "query.txt"


def generateInvertedIndex():
    invertedIndex = {}
    tokenDict = {}
    files = os.listdir(INPUT_FOLDER)
    for file in files:
        contents = open(INPUT_DIRECTORY + "/" + file, "r").read()
        words = contents.split()
        length = len(words)
        file = file[:-4]
        tokenDict[file] = length
        for i in range(length):
            word = words[i]
            if word not in invertedIndex.keys():
                docIDCount = {file : 1}
                invertedIndex[word] = docIDCount
            elif file in invertedIndex[word].keys():
                invertedIndex[word][file] += 1
            else:
                docIDCount = {file : 1}
                invertedIndex[word].update(docIDCount)
    return invertedIndex


def findTFIDF(term, doc, invertedIndex, docWordCount):
    tf = invertedIndex[term][doc]/docWordCount[doc]
    idf = 1.0 + (log(N/(invertedIndex[term][doc] + 1.0)))
    return tf, idf


def generateDocWordCount():
    docWordCount = {}
    files = os.listdir(INPUT_FOLDER)
    for file in files:
        doc = open(INPUT_FOLDER + "/" + file,"r").read().split()
        docWordCount[file[:-4]] = len(doc)
    return docWordCount


def generateTFIDF(invertedIndex, docWordCount):
    tfidf = {}
    for term in invertedIndex.keys():
        tfidf[term] = {}
        for doc in invertedIndex[term]:
            tf, idf = findTFIDF(term, doc, invertedIndex, docWordCount)
            tfidf[term][doc] = tf*idf
    return tfidf


def queryParser(query):
    file = open(query,'r').read().splitlines()
    queries = []
    for query in file:
        queries.append(query.split())
    return queries


def findDocScore(doc,tfidf):
    docScore = 0
    for term in tfidf:
        if doc in tfidf[term].keys():
            docScore += tfidf[term][doc]
    return docScore


def getScoredDocs(query, tfidf):
    queryIndex = {}
    docScoreList = {}
    for term in query:
        if term in tfidf:
            queryIndex[term] = tfidf[term]
        else:
            queryIndex[term] = {}
    for term in queryIndex:
        for doc in queryIndex[term]:
            if doc not in docScoreList.keys():
                docScore = findDocScore(doc, queryIndex) 
                docScoreList[doc] = docScore
    return docScoreList


def writeToFile(queries, tfidf):
    queryID = 1
    file = open(TF_IDF_SCORE_LIST, "w")       
    for query in queries:
        TFIDFScoreList = getScoredDocs(query, tfidf)
        sortedScoreList = sorted(TFIDFScoreList.items(), key=lambda x:x[1], reverse=True)
        for rank in range(100):
            text = str(queryID) +  "   " + "Q0" +  "   " + str(sortedScoreList[rank][0]) + "   " + str(rank+1) +  "   " + str(sortedScoreList[rank][1]) +  "   " + "TFIDF" +"\n"
            file.write(text)
        file.write("\n\n ---------------------------------------------------------------------------------------\n\n\n")
        queryID += 1
    file.close()


def main():
    invertedIndex = generateInvertedIndex()
    docWordCount = generateDocWordCount()
    tfidf = generateTFIDF(invertedIndex, docWordCount)
    queries = queryParser(QUERY_FILE)
    writeToFile(queries, tfidf)
main()

