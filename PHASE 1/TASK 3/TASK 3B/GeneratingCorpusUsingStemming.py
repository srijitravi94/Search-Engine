import os
from os.path import exists
CURRENT_DIRECTORY = os.getcwd()
OUTPUT_FOLDER = path = os.path.join(CURRENT_DIRECTORY,'CORPUS')


def generateStemmedCorpus():
    os.mkdir(OUTPUT_FOLDER)
    page = open("cacm_stem.txt").read()
    findHashSymbol = page.find('#')
    while findHashSymbol != -1:
        docID = page[findHashSymbol + 2: page.find("\n",findHashSymbol + 2)]
        nextHashSymbol = page.find('#',page.find("\n",findHashSymbol + 2))
        contents = page[findHashSymbol + 2 : nextHashSymbol]
        if len(docID) == 1:
            outputFileName = "CACM-000" + docID
        if len(docID) == 2:
            outputFileName = "CACM-00" + docID
        if len(docID) == 3:
            outputFileName = "CACM-0" + docID
        if len(docID) == 4:
            outputFileName = "CACM-" + docID
        outputFile = open(OUTPUT_FOLDER+ "/" + outputFileName +".txt",'w')
        outputFile.write(contents[len(docID):])
        findHashSymbol = page.find('#',nextHashSymbol)
generateStemmedCorpus()