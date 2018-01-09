import os
from math import log


QUERY = "cacm_stem.query.txt"
BM_25_SCORE_LIST = "BM25_SCORE_STEMMED_LIST.txt"
CACM_REL = "cacm.rel.txt"
INPUT_DIRECTORY = "CORPUS"
INPUT_FOLDER = os.getcwd() + "/" + INPUT_DIRECTORY
k1 = 1.2
k2 = 100
b = 0.75
N = len(os.listdir(INPUT_FOLDER))


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


def queryParser(query):
    file = open(query,'r').read().splitlines()
    queries = []
    for query in file:
        queries.append(query.split())
    return queries


def queryFrequency(query):
    queryFreq = {}
    for term in query:
        if term in queryFreq.keys():
            queryFreq[term] += 1
        else:
            queryFreq[term] = 1
    return queryFreq


def calculateLength():
    fileLengths = {}
    files = os.listdir("CORPUS")
    for file in files:
        doc = open("CORPUS/" + file,'r').read()
        file = file[:-4]
        fileLengths[file] = len(doc.split())
    return fileLengths


def calculateAverageLength(fileLengths):
    avgLength = 0
    for file in fileLengths.keys():
        avgLength += fileLengths[file]
    return avgLength/N


def calculateBM25(n, f, qf, r, N, dl, avdl, R):
    K = k1 * ((1 - b) + b * (float(dl) / float(avdl)))
    Q1 = log(((r + 0.5) / (R - r + 0.5)) / ((n - r + 0.5) / (N - n - R + r + 0.5)))
    Q2 = ((k1 + 1) * f) / (K + f)
    Q3 = ((k2 + 1) * qf) / (k2 + qf)
    return Q1 * Q2 * Q3


def findr(listOfDocs, relDocs):
    count = 0
    for doc in listOfDocs:
        if doc in relDocs:
            count += 1
    return count


def getRelevantList(queryID, docList):
    file = open(CACM_REL, "r").read().splitlines()
    relList = []
    relDocs = []
    for line in file:
        values = line.split()
        if values[0] == str(queryID):
            relList.append(values[2])
    for doc in docList.keys():
        if doc in relList:
            relDocs.append(doc)
    return relDocs


def findDocumentsForQuery(query, invertedIndex, fileLengths, queryID):
    queryFreq = queryFrequency(query)
    avdl = calculateAverageLength(fileLengths)
    BM25ScoreList = {}
    for doc in fileLengths.keys():
        BM25ScoreList[doc] = 0
    relevantList = getRelevantList(queryID, fileLengths)
    R = len(relevantList)
    for term in query:
        if term in invertedIndex.keys():
            qf = queryFreq[term]
            docDict = invertedIndex[term]
            r = findr(invertedIndex[term], relevantList)
            for doc in docDict:
                n = len(docDict)
                f = docDict[doc]
                dl = fileLengths[doc]
                BM25 = calculateBM25(n, f, qf, r, N, dl, avdl, R)
                BM25ScoreList[doc] += BM25
    return BM25ScoreList


def writeToFile(queries, invertedIndex, fileLengths):
    queryID = 1
    file = open(BM_25_SCORE_LIST, "w")       
    queryNames = open(QUERY, 'r').read().splitlines()
    for query in queries:
        BM25ScoreList = findDocumentsForQuery(query, invertedIndex, fileLengths, queryID)
        sortedScoreList = sorted(BM25ScoreList.items(), key=lambda x:x[1], reverse=True)
        for rank in range(100):
            text = str(queryID) +  "   " + "Q0" +  "   " + str(sortedScoreList[rank][0]) + "   " + str(rank+1) +  "   " + str(sortedScoreList[rank][1]) +  "   " + "BM25" +"\n"
            file.write(text)
        file.write("\n\n ---------------------------------------------------------------------------------------\n\n\n")
        queryID += 1
    file.close()


def main():
    queries = queryParser(QUERY)
    invertedIndex = generateInvertedIndex()
    fileLengths = calculateLength()
    writeToFile(queries, invertedIndex, fileLengths)
main()
