import os


INPUT_DIRECTORY = os.getcwd()

RELEVANT_FILE = "cacm.rel.txt"

BM25_SCORE_LIST = "BM25_SCORE_LIST_FOR_EVALUATION.txt"
BM25_SCORE_LIST_STOPPED_LIST = "BM25_SCORE_STOPPED_LIST_FOR_EVALUATION.txt"
LUCENE_SCORE_LIST = "LUCENE_SCORE_LIST_FOR_EVALUATION.txt"
LUCENE_SCORE_LIST_STOPPED_LIST = "LUCENE_SCORE_STOPPED_LIST_FOR_EVALUATION.txt"
TF_IDF_SCORE_LIST = "TF_IDF_SCORE_LIST_FOR_EVALUATION.txt"
TF_IDF_SCORE_LIST_STOPPED_LIST = "TF_IDF_SCORE_STOPPED_LIST_FOR_EVALUATION.txt"
PSEUDO_RELEVANCE_BM25_SCORE_LIST = "PSEUDO_RELEVANCE_BM25_SCORE_LIST_FOR_EVALUATION.txt"
SMOOTHED_MODEL_SCORE_LIST = "SMOOTHED_MODEL_SCORE_LIST_FOR_EVALUATION.txt"
MRR_SCORES_FILE_NAME = "MRR_SCORES.txt"
MAP_SCORES_FILE_NAME = "MAP_SCORES.txt"


def getScoredList(FILE_NAME):
    scoreDict = {}
    file = open(INPUT_DIRECTORY + "/" + FILE_NAME, "r")
    for line in file.readlines():
        query_key = int(line.split()[0])
        if query_key not in scoreDict.keys():
            scoreDict[query_key] = [line[:-1]]
        else:
            content = scoreDict.get(query_key)
            content.append(line[:-1])
    file.close()
    return scoreDict


def calculateMRR(relDict, scoreDict, FILE_NAME, NO_OF_QUERIES):
    queryID = 1
    rr = 0
    file = open(MRR_SCORES_FILE_NAME,'a')
    while queryID <= NO_OF_QUERIES:
        if relDict.get(queryID):
            relDocList = relDict[queryID]
            scoredDocList = scoreDict[queryID]
            for doc in scoredDocList:
                flag = False
                docID = doc.split()[2]
                for relDoc in relDocList:
                    if docID == relDoc.split()[2]:
                        rr += 1.0 / float(doc.split()[3])
                        flag = True
                        break
                if flag == True:
                    break
        queryID += 1
    mrr = rr / float(NO_OF_QUERIES)
    file.write(str(FILE_NAME[:-4]) + "  :  " + str(mrr) + "\n")


def calculatePK(relDict, scoreDict, FILE_NAME, NO_OF_QUERIES):
    p5 = {}
    p20 = {}
    queryID = 1
    file = FILE_NAME[:FILE_NAME.rindex('.')]
    filepk5 = open(file+"_P5_SCORE.txt",'w')
    filepk20 = open(file+"_P20_SCORE.txt",'w')
    while queryID <= NO_OF_QUERIES:
        if not relDict.get(queryID):
            p5[queryID] = 0.0
            p20[queryID] = 0.0
            queryID += 1
            continue
        relDocList = relDict[queryID]
        top5Scorelist = scoreDict[queryID][:5]
        top20Scorelist = scoreDict[queryID][:20]
        relDocCounterTop5 = 0
        for doc in top5Scorelist:
            docID = doc.split()[2]
            for rel_doc in relDocList:
                if docID == rel_doc.split()[2]:
                    relDocCounterTop5 += 1
        p5[queryID] = relDocCounterTop5/5
        filepk5.write(str(queryID) + " "+ str(p5[queryID]) +" PK5\n")
        relDocCounterTop20 = 0
        for doc in top20Scorelist:
            docID = doc.split()[2]
            for rel_doc in relDocList:
                if docID == rel_doc.split()[2]:
                    relDocCounterTop20 += 1

        p20[queryID] = relDocCounterTop20/20
        filepk20.write(str(queryID) + " "+ str(p20[queryID]) +" PK20\n")
        queryID += 1
    filepk5.close()
    filepk20.close()


def calculatePrecisionRecall(relDict, scoreDict, FILE_NAME, NO_OF_QUERIES):
    precisionDict = {}
    recallDict = {}
    totalAvgPrecision = 0
    file = FILE_NAME[:FILE_NAME.rindex('.')]
    prfile = open(file+"_PRECISION-RECALL.txt",'w')
    for query in scoreDict:
        avgPrecision = 0
        docCounter = 0
        found = 0
        totalPrecision = 0
        if not relDict.get(query):
            precisionDict[query] = []
            recallDict[query] = []
            prfile.write("No relevant set for QUERY "+ str(query) + "\n\n")
            continue
        relDocList = relDict[query]
        totalRelDocs = len(relDocList)
        precisionDict[query] = []
        recallDict[query] = []
        for doc in scoreDict[query]:
            docCounter +=1
            docID = doc.split()[2]
            docRank = doc.split()[3]
            docScore = doc.split()[4]
            fflag = False
            for relDoc in relDocList:
                if docID ==  relDoc.split()[2]:
                    fflag = True
                    break;
            if fflag:
                found += 1
                precision = float(found) / float(docCounter)
                totalPrecision = totalPrecision + precision
                precisionDict[query].append({docID : precision})
                recall = float(found) / float(totalRelDocs)
                recallDict[query].append({docID : recall})
                prfile.write(str(query) + " Q0 " + docID + " " + str(docRank) + " " + str(docScore) + " R " + str(precision)
                             + " " + str(recall) +"\n")
            else:
                precision = float(found) / float(docCounter)
                precisionDict[query].append({docID : precision})
                recall = float(found) / float(totalRelDocs)
                recallDict[query].append({docID : recall})
                prfile.write(str(query) + " Q0 " + docID + " " + str(docRank) + " " + str(docScore) + " N " + str(precision)
                             + " " + str(recall) +"\n")
        if found != 0:
            avgPrecision = avgPrecision + float(totalPrecision) / float(found)
        else:
            avgPrecision = 0
        prfile.write("\nAverage Precision for QUERY "+ str(query) +" : " + str(avgPrecision)+"\n\n")
        totalAvgPrecision = totalAvgPrecision + avgPrecision
    MAP = float(totalAvgPrecision) / float(NO_OF_QUERIES)
    MAPfile = open(MAP_SCORES_FILE_NAME, "a")
    MAPfile.write(str(FILE_NAME[:-4]) + "  :  " + str(MAP) + "\n")
    prfile.write("\nMAP: " + str(MAP)+"\n")
    prfile.close()


def generateResults(relDict, FILE_NAME):
    NO_OF_QUERIES = len(relDict.keys())
    scoreDict = getScoredList(FILE_NAME)
    calculateMRR(relDict, scoreDict, FILE_NAME, NO_OF_QUERIES)
    calculatePK(relDict, scoreDict, FILE_NAME, NO_OF_QUERIES)
    calculatePrecisionRecall(relDict, scoreDict, FILE_NAME, NO_OF_QUERIES)


def main():
    relDict = getScoredList(RELEVANT_FILE)
    generateResults(relDict, BM25_SCORE_LIST)
    generateResults(relDict, BM25_SCORE_LIST_STOPPED_LIST)
    generateResults(relDict, LUCENE_SCORE_LIST)
    generateResults(relDict, LUCENE_SCORE_LIST_STOPPED_LIST)
    generateResults(relDict, TF_IDF_SCORE_LIST)
    generateResults(relDict, TF_IDF_SCORE_LIST_STOPPED_LIST)
    generateResults(relDict, PSEUDO_RELEVANCE_BM25_SCORE_LIST)
    generateResults(relDict, SMOOTHED_MODEL_SCORE_LIST)
main()