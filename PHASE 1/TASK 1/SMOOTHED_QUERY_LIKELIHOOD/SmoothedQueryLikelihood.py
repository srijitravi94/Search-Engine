import math
import os


INPUT_DIRECTORY = "CORPUS"
INPUT_FOLDER = os.getcwd() + "/" + INPUT_DIRECTORY
QUERY = "query.txt"
SMOOTHED_MODEL_SCORE_LIST = "SMOOTHED_MODEL_SCORE_LIST.txt"
LAMBDA = 0.35


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


def calculateLength():
    fileLengths = {}
    files = os.listdir("CORPUS")
    for file in files:
        doc = open("CORPUS/" + file,'r').read()
        file = file[:-4]
        fileLengths[file] = len(doc.split())
    return fileLengths


def queries(fileName):
    f = open(fileName,'r')
    queryList = []
    for line in f:
        line=" ".join(line.split())
        line=line.strip() 
        if line[-1] == '\n':            # Remove new line character
            queryList.append(line[0:-1])
        elif line[-1] == ' ':           # Remove last space
            queryList.append(line[0:-1])
        else:
            queryList.append(line)

    queryProcessor(queryList)
    return queryList


def queryProcessor(querySet):
    queryTerms = {}
    for query in querySet:
        queryTerms[query] = query.split(" ")      
    return queryTerms


# write the final maximum results document to a file
def rankedDocsFinal(docWeights, qid, maximumResults):
    file = open(SMOOTHED_MODEL_SCORE_LIST, "a")
    sortedList = sorted(docWeights, key=docWeights.__getitem__)
    top = sortedList[-(maximumResults):]
    top.reverse()
    rank = 0
    for doc in top:
        rank += 1
        text= str(qid+1) + "   " + "Q0" + "   " + str(doc) + "   " + str(rank) + "   " + str(docWeights[doc]) + "   " + "SmoothedQueryLikelihood" +"\n"
        file.write(text)
    file.write("\n\n ---------------------------------------------------------------------------------------\n\n\n")


#calculating Query Likelihood Score for each query term
def SQLScore(maximumResults, total_collection, index, querySet, uniqueDocuments, doclength):
    qid = -1
    i=0
    score_accumulator=0
    queryTerms = queryProcessor(querySet)
    for query in querySet:
        qid += 1
        docWeights = {}
        for document in uniqueDocuments:
            documentScore = 0
            for queryTerm in list(set(queryTerms[query])):
                 if queryTerm in index.keys():
                    if document in index[queryTerm]:
                        termWeight_doc = index[queryTerm][document]
                    else:
                        termWeight_doc = 0
                    modD=doclength[document]
                    termWeight_collection= sum(index[queryTerm].values())
                    queryFreq_by_modD= termWeight_doc/modD
                    collectionFreq_by_total_collection= termWeight_collection/total_collection
                    score = (((1-LAMBDA)*queryFreq_by_modD)+(LAMBDA*collectionFreq_by_total_collection))
                    score_accumulator+=math.log(score)
            docWeights[document] = score_accumulator
            score_accumulator=0
        rankedDocsFinal(docWeights, qid, maximumResults)


# Main. The program starts from here
def main():
    index = generateInvertedIndex()
    maximumResults = 100
    uniqueDocuments=[]
    uniqueDocuments = [file[:-4] for file in os.listdir(INPUT_FOLDER)] #unique_docs(index) # Set of Docs
    total_docs = len(uniqueDocuments)          # Size of Corpus
    doclength = calculateLength()              # Size of each document in a Dictionary
    querySet = queries(QUERY)                  # Set of Queries
    total_collection=sum(doclength.values())
    SQLScore(maximumResults, total_collection, index, querySet, uniqueDocuments, doclength)      # Function call which computes document score
main()

