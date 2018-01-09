import os

stopwords = open('common_words.txt').read().split()

INPUT_DIRECTORY = "CORPUS"
INPUT_FOLDER = os.getcwd() + "/" + INPUT_DIRECTORY
OUTPUT_DIRECTORY = os.getcwd() + "/" + "STOP_CORPUS"
files = os.listdir(INPUT_FOLDER)

def removeCommonWords():
	if not os.path.exists(OUTPUT_DIRECTORY):
		os.makedirs(OUTPUT_DIRECTORY)
	for file in files:
		contents = open(INPUT_DIRECTORY + "/" + file, "r").read().split()
		for stop in stopwords:
			for content in contents:
				if content==stop:
					contents.remove(content)
		outfile_name = file

		with open(OUTPUT_DIRECTORY + "/" + outfile_name, 'a') as out_link:
	            for content in contents:
	            	out_link.write(content)
	            	out_link.write(" ")
	            out_link.close()

def main():
	removeCommonWords()
main()
    
    	
        