FOLDERS:
---------------------------------------------------------------------------------------------------------------------------------------------------------
CORPUS
INPUT_FOLDER
PHASE 1
PHASE 2
PHASE 3
---------------------------------------------------------------------------------------------------------------------------------------------------------
GeneratingCorpus.py :
A program for prasing and tokenizing the input documents

It takes the given 3204 raw HTML documents as input and the output is generated 
in the CORPUS folder

Procedure to run:
python GeneratingCorpus.py

--------------------------
CORPUS:
The 3204 output parsed text documents generated for GeneratingCorpus.py
---------------------------------------------------------------------------------------------------------------------------------------------------------
INPUT_FOLDER:
Consists of all the documents given as part of the question.
--------------------------
INPUT_FOLDER -> cacm:
Consists of the 3204 raw HTML input documents
---------------------------------------------------------------------------------------------------------------------------------------------------------



PHASE 1 -> TASK 1 -> BM25:
Consists of all the documents relating to BM25 Baseline run
--------------------------
CORPUS:
The 3204 input parsed documents for BM25 scoring
--------------------------
BM25.py:
The program is used for ranking documents based on BM25 algorithm

Procedure to run:
python BM25.py
--------------------------
BM25_SCORE_LIST.txt:
The output of ranked documents based on BM25
--------------------------
cacm.rel.txt :
The set of relevance information
--------------------------
query.txt:
Contains the list of queries submitted

--------------------------------------------------------------------------------
PHASE 1 -> TASK 1 -> Lucene:
Consists of all the documents relating to Lucene Baseline run
--------------------------
CORPUS:
The 3204 input parsed documents for Lucene scoring
--------------------------
JAR FILES:
Consists of the JAR files to be imported for Lucene (Version- 4.7.2)
--------------------------
LUCENE_SCORE_LIST.txt:
The output file generated for Lucene ranking
--------------------------
LuceneImplementation.java
The java code implementing the ranking of documents based on Lucene

Procedure to run:
javac HW4.java
java HW4
 When prompted;
 Enter the FULL path where the index will be created: (e.g. /Usr/index or c:\temp\index)
 **Enter the path where the output file should be located**
 When prompted;
 Enter the FULL path to add into the index (q=quit): (e.g. /home/mydir/docs or c:\Users\mydir\docs)
[Acceptable file types: .xml, .html, .html, .txt]
 ** Enter the path of parsed_docs folder **
 ** Enter "q" to quit **
--------------------------
query.txt:
Contains the list of queries submitted

--------------------------------------------------------------------------------
PHASE 1 -> TASK 1 -> SMOOTHED_QUERY_LIKELIHOOD:
Consists of all the documents relating to Smoothed Query Likelihood Baseline run
--------------------------
CORPUS:
The 3204 input parsed documents for SmoothedQueryLikelihood scoring
--------------------------
query.txt:
Contains the list of queries submitted
--------------------------
SMOOTHED_MODEL_SCORE_LIST.txt
The output file generated for Smoothed query likelihood ranking
--------------------------
SmoothedQueryLikelihood.py:
The python program to rank the documents based on Smoothed query likelihood model

Procedure to run:
python SmoothedQueryLikelihood.py
--------------------------------------------------------------------------------
PHASE 1 -> TASK 1 -> TF-IDF:
Consists of all the documents relating to TF-IDF Baseline run
--------------------------
CORPUS:
The 3204 input parsed documents for TF-IDF scoring
--------------------------
query.txt:
Contains the list of queries submitted
--------------------------
TF_IDF_SCORE_LIST.txt :
The output file generated of ranked documents based on TF_IDF mechanism
--------------------------
TF-IDF.py:
The python programm for ranking documents based on TF-IDF algorithm

Procedure to run:
python TF-IDF.py
--------------------------------------------------------------------------------



PHASE 1 -> TASK 2 -> PSEUDO_RELEVANCE_FEEDBACK:
Consists of all the documents relating to Pseudo relevance feedback run
--------------------------
CORPUS:
The 3204 input parsed documents for PseudoRelevanceFeedback
--------------------------
query.txt:
Contains the list of queries submitted
--------------------------
cacm.rel.txt:
Consists of the relevance information
--------------------------
PSEUDO_RELEVANCE_BM25_SCORE_LIST.txt:
Consists of the output of the pesudo relevance ranking algorithm
--------------------------
PseudoRelevanceFeedbackBM25.py:
The python program for pesudo relevance feedback algorithm

Procedure to run:
python PseudoRelevanceFeedbackBM25.py

--------------------------------------------------------------------------------


PHASE 1 -> TASK 3 -> TASK 3A:
Consists of all the files relating to the 3 basseline runs for Stopped corpus
--------------------------
CORPUS:
The 3204 input parsed documents
--------------------------
STOP_CORPUS:
The 3204 documents generated after stopping operation
--------------------------
common_words.txt
The list of given stop words
--------------------------
common_words_parse.py:
The python program for removing the stopped words from the parsed corpus

Procedure to run:
python common_words_parse.py
--------------------------
BM25.py:
The python program for BM25 algorithm for ranking the documents for which Stopping
operation had been performed.

Procedure to run:
As mentioned before
--------------------------
BM25_SCORE_STOPPED_LIST.txt:
The BM25 ouput file generated for stopped corpus
--------------------------
cacm.rel.txt:
The relevance information provided
--------------------------
LUCENE_SCORE_STOPPED_LIST.txt:
The ouput ranked documents generated for Stopped words using Lucene
--------------------------
LuceneImplementation.java:
The Lucene program for ranking the stopped list of documents using Lucene

Procedure to run:
As mentioned before
--------------------------
TF_IDF_SCORE_STOPPED_LIST.txt:
The output file generated for stopped list of documents using TF-IDF algorithm
--------------------------
TF-IDF.py:
The python program for ranking documents using TF-IDF

Procedure to run:
As mentioned before

--------------------------------------------------------------------------------



PHASE 1 -> TASK 3 -> TASK 3B:
Consists of all the files relating to the 3 basseline runs for stemmed corpus
--------------------------
CORPUS:
The 3204 input parsed documents
--------------------------
cacm.rel.txt:
The relevance information provided
--------------------------
cacm_stem.query.txt:
The set of stemmed query provided
--------------------------
cacm_stem.txt:
It consists of the raw unparsed stemmed documents
--------------------------
GeneratingCorpusUsingStemming.py:
The python program for parsing the documents using the cacm_stem.txt
--------------------------
BM25_SCORE_STEMMED_LIST.txt:
The outpur file generated after BM25 ranking on stemmed corpus
--------------------------
BM25ForStemming.py:
The  program for ranking the documents based on BM25 algorithm for stemmed corpus

Procedure to run:
As mentioned before
--------------------------
LUCENE_SCORE_STEMMED_LIST.txt:
The output file generated for stmmed corpus using Lucene
--------------------------
LuceneImplementationStemmedList.java
The program for ranking stemmed documents using Lucene

Procedure to run:
As mentioned before
--------------------------
TF_IDF_SCORE_STEMMED_LIST.txt:
The outpur file generated for ranked documents using TF-IDF
--------------------------
TF-IDF-ForStemming.py:
The program for ranking stemmed documents using TF-IDF

Procedure to run:
As mentioned before
---------------------------------------------------------------------------------------------------------------------------------------------------------



PHASE 2 -> SNIPPET_GENERATION :
Consists of the documents relating to implementation of Snippet generation
--------------------------
cacm:
The set of 3204 unprocessed documents
--------------------------
lucene_score ->	LUCENE_SCORE_LIST.txt:
The ranked documents generated from Lucene program
--------------------------
cacm.query:
The set of queries submitted
--------------------------
SnippetGeneration.py:
The program for generated snippet based from Lucene output of ranked documents

Procedure to run:
python SnippetGeneration.py

Requirements:
import colorama (for Windows and run in command prompt)

Output generated:
The output is generated in command prompt and the query terms in documents 
are highlighted
--------------------------
unprocessed_query.txt:
The set of queries generated just removing the tags
---------------------------------------------------------------------------------------------------------------------------------------------------------



PHASE 3 -> SNIPPET_GENERATION :
Consists the files relating to the evaluation of eight distinct runs of 64 queries
--------------------------
cacm.rel.txt:
Consists of the relevance information
--------------------------
Evaluation.py:
Program for computing the various evaluation measure:
1- MAP
2- MRR
3- P@K, K=5 and K=20
4- Precision & Recall
--------------------------
MAP_SCORES.txt:
The ouput file consisting of the Mean average Precision scores of the documents
--------------------------
MRR_SCORES.txt:
The output file consisting of the Mean Reciprocal Rank scores of the documents
--------------------------
BM25_SCORE_LIST_FOR_EVALUATION.txt:
The ranked list of documents generated for BM25 ranking algorithm
--------------------------
BM25_SCORE_LIST_FOR_EVALUATION_P5_SCORE.txt:
The precision score generated using BM25 at K=5
--------------------------
BM25_SCORE_LIST_FOR_EVALUATION_P20_SCORE.txt:
The precision score generated using BM25 at K=20
--------------------------
BM25_SCORE_LIST_FOR_EVALUATION_PRECISION-RECALL.txt:
The output generated contains the Precision and Recall of documents ranked using BM25
--------------------------
BM25_SCORE_STOPPED_LIST_FOR_EVALUATION.txt:
The ranked list of stopped documents generated for BM25 ranking algorithm
--------------------------
BM25_SCORE_STOPPED_LIST_FOR_EVALUATION_P5_SCORE.txt:
The precision score generated using BM25 for stopped corpus at K=5
--------------------------
BM25_SCORE_STOPPED_LIST_FOR_EVALUATION_P20_SCORE.txt:
The precision score generated using BM25 for stopped corpus at K=20
--------------------------
BM25_SCORE_STOPPED_LIST_FOR_EVALUATION_PRECISION-RECALL.txt:
The output generated for stopped corpus contains the Precision and Recall of 
documents ranked using BM25
--------------------------
LUCENE_SCORE_LIST_FOR_EVALUATION.txt:
The ranked list of documents generated using Lucene
--------------------------
LUCENE_SCORE_LIST_FOR_EVALUATION_P5_SCORE.txt:
The precision score generated using Lucene at K=5
--------------------------
LUCENE_SCORE_LIST_FOR_EVALUATION_P20_SCORE.txt:
The precision score generated using Lucene at K=20
--------------------------
LUCENE_SCORE_LIST_FOR_EVALUATION_PRECISION-RECALL.txt
The precision and recall scores generated for Lucene
--------------------------
LUCENE_SCORE_STOPPED_LIST_FOR_EVALUATION.txt:
The ranked list of stopped documents dgenerated using Lucene
--------------------------
LUCENE_SCORE_STOPPED_LIST_FOR_EVALUATION_P5_SCORE.txt:
The precision score for stopped corpus using Lucene at K=5
--------------------------
LUCENE_SCORE_STOPPED_LIST_FOR_EVALUATION_P20_SCORE.txt:
The precision score for stopped corpus using Lucene at K=20
--------------------------
LUCENE_SCORE_STOPPED_LIST_FOR_EVALUATION_PRECISION-RECALL.txt:
The precision and recall scores generated for stopped corpus using Lucene
--------------------------
PSEUDO_RELEVANCE_BM25_SCORE_LIST_FOR_EVALUATION.txt
PSEUDO_RELEVANCE_BM25_SCORE_LIST_FOR_EVALUATION_P5_SCORE.txt
PSEUDO_RELEVANCE_BM25_SCORE_LIST_FOR_EVALUATION_P20_SCORE.txt
PSEUDO_RELEVANCE_BM25_SCORE_LIST_FOR_EVALUATION_PRECISION-RECALL.txt


The evaluation measures generated for Peseudo relevance algorithm
--------------------------
SMOOTHED_MODEL_SCORE_LIST_FOR_EVALUATION.txt
SMOOTHED_MODEL_SCORE_LIST_FOR_EVALUATION_P5_SCORE.txt
SMOOTHED_MODEL_SCORE_LIST_FOR_EVALUATION_P20_SCORE.txt
SMOOTHED_MODEL_SCORE_LIST_FOR_EVALUATION_PRECISION-RECALL.txt

The evaluation measures generated for Smoothed query likelihood model
--------------------------
TF_IDF_SCORE_LIST_FOR_EVALUATION.txt
TF_IDF_SCORE_LIST_FOR_EVALUATION_P5_SCORE.txt
TF_IDF_SCORE_LIST_FOR_EVALUATION_P20_SCORE.txt
TF_IDF_SCORE_LIST_FOR_EVALUATION_PRECISION-RECALL.txt

The evaluation measures generated for TF-IDF
--------------------------
TF_IDF_SCORE_STOPPED_LIST_FOR_EVALUATION.txt
TF_IDF_SCORE_STOPPED_LIST_FOR_EVALUATION_P5_SCORE.txt
TF_IDF_SCORE_STOPPED_LIST_FOR_EVALUATION_P20_SCORE.txt
TF_IDF_SCORE_STOPPED_LIST_FOR_EVALUATION_PRECISION-RECALL.txt

The evaluation measures generated for TF-IDF on stopped corpus

---------------------------------------------------------------------------------------------------------------------------------------------------------

