
# Importing required libraries
import os
import re
from bs4 import BeautifulSoup


# Declaring global variables
INPUT_DIRECTORY = "INPUT_FOLDER"
CACM_DIRECTORY = "cacm"
CACM_QUERY = "cacm.query.txt"
QUERY = "query.txt"
OUTPUT_DIRECTORY = "CORPUS"
INPUT_FOLDER = os.getcwd() + "/" + INPUT_DIRECTORY + "/" + CACM_DIRECTORY


# Function to generate link and content dictionary
def getFileContents():
    files = os.listdir(INPUT_FOLDER)
    fileDictionary = {}
    for file in files:
        key = file.split(".")[0]
        value = open(INPUT_FOLDER + "/" + file, "r")
        fileDictionary[key] = value.read()
    return fileDictionary


# Function to check whether the given word/text is float
def isFloat(word):
    word = re.sub('[.,]', '', word)
    try:
        float(word)
        return True
    except ValueError:
        return False


# Function to remove punctuations
def removeHyphenAtStartAndEnd(word):
    if word:
        while word[-1] == '-':
            word = word[:len(word)-1]
    if word:
        while word[0] == '-':
            word = word[1:]
    return word


# Function to extract text
def extractText():
    fileDictionary = {}
    files = getFileContents()
    for file in files:
        fileContent = files[file]
        soup = BeautifulSoup(fileContent, "html.parser")
        content = soup.find('pre').text
        symbols = re.compile('[_!@\s#$%=+~()}{\][^?&*:;\\/|<>"\']')
        content = re.sub(symbols, ' ', content)
        words = content.split()
        fileDictionary[file] = words
    return fileDictionary


def addText(content):
    if isFloat(content):
        text = content.lower() + " "
    else:
        text = re.sub('[.,]', '', content.lower()) + " "
    return text    


# Function to store file and extracted text in a dictionary
def convertToText():
    fileDictionary = extractText()
    for file in fileDictionary:
        contents = fileDictionary[file]
        text = ""
        for content in contents:
            text += removeHyphenAtStartAndEnd(addText(content))
        fileDictionary[file] = text
    return fileDictionary


# Function to write the content to a file
def writeFile(name, content):
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.makedirs(OUTPUT_DIRECTORY)
    filename = name + str(".txt")
    path = os.getcwd() + '/' + OUTPUT_DIRECTORY
    files = os.listdir(path)
    if filename not in files:
        file = open(OUTPUT_DIRECTORY + "/" + filename, "w")
        file.write(str(content))
    else:
        file = open(OUTPUT_DIRECTORY + "/" + name + "1" + str(".txt"), "w")
        file.write(str(content))
    file.close()


def processQuery(fileContents):
    query = fileContents[fileContents.find('</DOCNO>')+8:fileContents.find('</DOC>')]
    symbols = re.compile('[_!@\s#$%=+~()}{\][^?&*:;\\/|<>"\']')
    query = re.sub(symbols, ' ', query)
    text = ''
    for term in query.split():
        text += removeHyphenAtStartAndEnd(addText(term))
    fileContents = fileContents[fileContents.find('</DOC>')+6:]
    return fileContents, text


def parseQuery():
    fileContents = open(INPUT_DIRECTORY + "/" + CACM_QUERY,"r").read()
    queryFile = open(INPUT_DIRECTORY + "/" + QUERY, "w")
    while fileContents.find("<DOC>") != -1:
        fileContents, query = processQuery(fileContents)
        queryFile.write(query + "\n")


# Main function
def main():
    fileDictionary = convertToText()
    for link in fileDictionary:
        writeFile(link, fileDictionary[link])
    parseQuery()    
main()

