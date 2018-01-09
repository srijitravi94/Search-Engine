import traceback
from os.path import exists
import os
import operator
from bs4 import BeautifulSoup
from colorama import *

CWD = os.getcwd()
CACM = path = os.path.join(CWD,'cacm')
LUCENE_SCORE_PATH = path = os.path.join(CWD,'lucene_score')

def processed_query(unprocessed_query):
    try:
        temp_list = []
        query = unprocessed_query[unprocessed_query.find('</DOCNO>')+8:unprocessed_query.find('</DOC>')]
        query = query.strip()
        temp_list = query.split()
        query = " ".join(temp_list)
        unprocessed_query = unprocessed_query[unprocessed_query.find('</DOC>')+6:]
        return unprocessed_query,query
    except Exception as e:
        print(traceback.format_exc())


def processing_query():
    try:
        if exists(CWD+"/unprocessed_query.txt"):
            os.remove(CWD+"/unprocessed_query.txt")
        unprocessed_query = open(CWD+"/cacm.query",'r').read()
        query_file = open(CWD+"/unprocessed_query.txt",'a')
        while unprocessed_query.find('<DOC>')!=-1:
            unprocessed_query, query = processed_query(unprocessed_query)
            if(unprocessed_query.find('<DOC>')==-1):
                query_file.write(query)
            else:
                query_file.write(query+"\n")
    except Exception as e:
        print(traceback.format_exc())

def ngram_snippet(queryTermList,file_name,n):

    try:
        lookahead = 40
        posttail = 50
        
        content = open(CACM+"/"+file_name+".html",'r').read()
        
        soup = BeautifulSoup(content, "html.parser")
        soup.prettify().encode("utf-8")
        doc_content = soup.find('pre').get_text()
        
        for i in range(len(queryTermList) - (n-1)):
            if n==3:
                term = queryTermList[i]+" "+queryTermList[i+1]+" "+queryTermList[i+2]
            elif n==2:
                term = queryTermList[i]+" "+queryTermList[i+1]
            else:
                term = queryTermList[i]

            
            if(doc_content.find(term)!=-1):
                start_index = max(doc_content.index(term)-lookahead, 0)
                if start_index!=0:
                    while start_index > 0:
                        if doc_content[(start_index-1):start_index] not in [" ","\n"]:
                            start_index-=1
                        else:
                            break
                sum = doc_content.index(term) +  len(term) + posttail
                end_index = min(sum, len(doc_content))
                if end_index!=len(doc_content):
                    while end_index < len(doc_content):
                        if doc_content[end_index:(end_index+1)] not in [" ","\n"]:
                            end_index+=1
                        else:
                            break
                first_part = doc_content[start_index:doc_content.index(term)]
                query_term_part = doc_content[doc_content.index(term):(doc_content.index(term)+len(term))]
                rest = doc_content[(doc_content.index(term)+len(term)):end_index]
                return first_part, query_term_part, rest
        return False, False, False
    except Exception as e:
        print(traceback.format_exc())



def generate_snippet(query,file_name):
    try:
        print("\n\nSNIPPET FOR QUERY-"+query+"in ")

        queryTermList = query.split()

        if len(queryTermList) > 2:
            first_part, query_term_part, rest = ngram_snippet(queryTermList,file_name,3)
            if first_part != False:
                print ("-------------DOCUMENT:"+file_name+"-----------------")
                
                print (first_part+" "+"\033[31;43m"+query_term_part+"\033[m"+" "+rest)
            else:
                first_part, query_term_part, rest = ngram_snippet(queryTermList,file_name,2)
                if first_part != False:
                    print ("-------------DOCUMENT:"+file_name+"-----------------")
                    print (first_part+" "+"\033[31;43m"+query_term_part+"\033[m"+" "+rest)
                else:
                    first_part, query_term_part, rest = ngram_snippet(queryTermList,file_name,1)
                    if first_part != False:
                        print ("-------------DOCUMENT:"+file_name+"-----------------")
                        print (first_part+" "+"\033[31;43m"+query_term_part+"\033[m"+" "+rest)
                    else:
                        print("no query term found in " + file_name)
        elif len(queryTermList) > 1:
            first_part, query_term_part, rest = ngram_snippet(queryTermList,file_name,2)
            if first_part != False:
                print ("-------------DOCUMENT:"+file_name+"-----------------")
                print (first_part+" "+"\033[31;43m"+query_term_part+"\033[m"+" "+rest)
            else:
                first_part, query_term_part, rest = ngram_snippet(queryTermList,file_name,1)
                if first_part != False:
                    print ("-------------DOCUMENT:"+file_name+"-----------------")
                    print (first_part+" "+"\033[31;43m"+query_term_part+"\033[m"+" "+rest)
                else:
                    print("no query term found in " + file_name)
        else:
            first_part, query_term_part, rest = ngram_snippet(queryTermList,file_name,1)
            if first_part != False:
                print ("-------------DOCUMENT:"+file_name+"-----------------")
                print (first_part+" "+"\033[31;43m"+query_term_part+"\033[m"+" "+rest)
            else:
                print("no query term found in " + file_name)
    except Exception as e:
        print(traceback.format_exc())

def lucene_out_ref(query_id):
    try:
        file_list = []
        doc_score_file = open(LUCENE_SCORE_PATH+"/LUCENE_SCORE_LIST.txt")
        for line in doc_score_file.readlines():
            column = line.split()
            #print("PARAMS[0]:",params[0])
            
            if column[0] == str(query_id):
                print(column[2])
                
                file_list.append(column[2])
        doc_score_file.close()
        return file_list
    except Exception as e:
        print(traceback.format_exc())

# Main. The program starts from here
if __name__ == "__main__" :
    try:
        init()
        processing_query()
        query_id = 0
        semi_processed_file = open('unprocessed_query.txt','r')
        for query in semi_processed_file.readlines():
            query_id+=1
            print("TOP 100 DOCUMENTS FOR QUERY ID:",query_id)
            list_of_files = lucene_out_ref(query_id)
            for file_name in list_of_files:                
                generate_snippet(query,file_name)
    except Exception as e:
        print(traceback.format_exc())


