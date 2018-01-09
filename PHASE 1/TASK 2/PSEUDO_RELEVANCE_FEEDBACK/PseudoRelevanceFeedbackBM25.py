import os
from math import log, sqrt


QUERY = "query.txt"
PSEUDO_RELEVANCE_BM_25_SCORE_LIST = "PSEUDO_RELEVANCE_BM25_SCORE_LIST.txt"
CACM_REL = "cacm.rel.txt"
INPUT_DIRECTORY = "CORPUS"
INPUT_FOLDER = os.getcwd() + "/" + INPUT_DIRECTORY
k1 = 1.2
k2 = 100
b = 0.75
ALPHA = 1
BETA = 0.75
GAMMA = 0.15
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


def queryFrequency(query, invertedIndex):
    queryFreq = {}
    for term in query:
        if term in queryFreq.keys():
            queryFreq[term] += 1
        else:
            queryFreq[term] = 1
    for term in invertedIndex:
        if term not in queryFreq.keys():
            queryFreq[term] = 0
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


def findDocs(k, sortedBM25Score, invertedIndex, relevancy):
    relIndex = {}
    nonRelIndex = {}
    if relevancy == "Relevant":
        for i in range(0, k):
            doc,doc_score = sortedBM25Score[i]
            relIndex = calculateDocsCount(doc, relIndex, invertedIndex)
        for term in invertedIndex:
            if term not in relIndex.keys():
                relIndex[term] = 0
        return relIndex
    elif relevancy == "Non-Relevant":
        for i in range(k+1,len(sortedBM25Score)):
            doc,doc_score = sortedBM25Score[i]
            nonRelIndex = calculateDocsCount(doc, nonRelIndex, invertedIndex)
        for term in invertedIndex:
            if term not in nonRelIndex.keys():
                nonRelIndex[term] = 0   
        return nonRelIndex


def calculateDocsCount(doc, docIndex, invertedIndex):
    doc= open(INPUT_FOLDER + "/" + doc + ".txt").read()
    for term in doc.split():
        if term in docIndex.keys():
            docIndex[term] += 1
        else:
            docIndex[term] = 1
    return docIndex


def findRelDocMagnitude(docIndex):
    mag = 0
    for term in docIndex:
        mag += float(docIndex[term]**2)
        mag = float(sqrt(mag))
    return mag


def findNonRelDocMagnitude(docIndex):
    mag = 0
    for term in docIndex:
        mag += float(docIndex[term]**2)
    mag = float(sqrt(mag))
    return mag


def findRocchioScore(term, queryFreq, relDocMag, relIndex, nonRelMag, nonRelIndex):
    Q1 = ALPHA * queryFreq[term] 
    Q2 = (BETA/relDocMag) * relIndex[term]
    Q3 = (GAMMA/nonRelMag) * nonRelIndex[term]
    rocchioScore = ALPHA * queryFreq[term] + (BETA/relDocMag) * relIndex[term] - (GAMMA/nonRelMag) * nonRelIndex[term]
    return rocchioScore


def findNewQuery(query, queryFreq, relDocMag, relIndex, nonRelMag, nonRelIndex, invertedIndex):
    updatedQuery = {}
    newQuery = query
    for term in invertedIndex:
        updatedQuery[term] = findRocchioScore(term, queryFreq, relDocMag, relIndex, nonRelMag, nonRelIndex)
    sortedUpdatedQuery = sorted(updatedQuery.items(), key=lambda x:x[1], reverse=True)
    if len(sortedUpdatedQuery)<20:
        loopRange = len(sortedUpdatedQuery)
    else:
        loopRange = 20
    for i in range(loopRange):
        term,frequency = sortedUpdatedQuery[i]
        if term not in query:
            newQuery +=  " "
            newQuery +=  term
    return newQuery


def pseudoRelevanceFeedbackScores(sortedBM25Score, query, invertedIndex, fileLengths, relevant_list, queryID):
    global feedbackFlag
    feedbackFlag += 1
    newQuery = query
    k = 10 # top 10 documents to be taken as relevant
    queryFreq = queryFrequency(query, invertedIndex)
    relIndex = findDocs(k, sortedBM25Score, invertedIndex, "Relevant")
    relDocMag = findRelDocMagnitude(relIndex)
    nonRelIndex = findDocs(k, sortedBM25Score, invertedIndex, "Non-Relevant")
    nonRelMag = findNonRelDocMagnitude(nonRelIndex)
    newQuery = findNewQuery(query, queryFreq, relDocMag, relIndex, nonRelMag, nonRelIndex, invertedIndex)
    PseudoRelevanceScoreList = findDocumentsForQuery(newQuery, invertedIndex, fileLengths, queryID)
    return PseudoRelevanceScoreList


def findDocumentsForQuery(query, invertedIndex, fileLengths, queryID):
    global feedbackFlag
    N = len(fileLengths.keys())
    queryFreq = queryFrequency(query, invertedIndex)
    avdl = calculateAverageLength(fileLengths)
    BM25ScoreList = {}
    relevantList = getRelevantList(queryID, fileLengths)
    R = len(relevantList)
    if type(query) != list:
        query = query.split()
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
                if doc in BM25ScoreList.keys():
                    BM25ScoreList[doc] += BM25
                else:
                    BM25ScoreList[doc] = BM25
    sortedBM25Score = sorted(BM25ScoreList.items(), key=lambda x:x[1], reverse=True)
    if feedbackFlag == 1:
        return pseudoRelevanceFeedbackScores(sortedBM25Score, query, invertedIndex , fileLengths, relevantList, queryID)
    elif feedbackFlag == 2:
        feedbackFlag = 1
        return BM25ScoreList


def writeToFile(queries, invertedIndex, fileLengths):
    global feedbackFlag
    queryID = 1
    file = open(PSEUDO_RELEVANCE_BM_25_SCORE_LIST, "w")       
    queryNames = open(QUERY, 'r').read().splitlines()
    for query in queries:
        feedbackFlag = 1
        PSRBM25ScoreList = findDocumentsForQuery(query, invertedIndex, fileLengths, queryID)
        sortedScoreList = sorted(PSRBM25ScoreList.items(), key=lambda x:x[1], reverse=True)
        for rank in range(100):
            text = str(queryID) +  "   " + "Q0" +  "   " + str(sortedScoreList[rank][0]) + "   " + str(rank+1) +  "   " + str(sortedScoreList[rank][1]) +  "   " + "PSR-BM25" +"\n"
            file.write(text)
        file.write("\n\n ---------------------------------------------------------------------------------------\n\n\n")
        print("Query" + str(queryID) + " Done!")
        queryID += 1
    file.close()


def main():
    queries = queryParser(QUERY)
    invertedIndex = generateInvertedIndex()
    fileLengths = calculateLength()
    writeToFile(queries, invertedIndex, fileLengths)
main()