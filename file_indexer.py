import pickle
import os
import re

'''
File Indexer**Write a program that indexes all files in a certain user-designated directory (folder). The program should construct a dictionary where the keys are all unique words in all the files (as described by the regular expression r"\w+"; treat the words as case-insensitive), and the value of each entry is a list of file names that contain the word. For instance, if the word “aloha” is mentioned in the files “early-internet.dat” and “hawaiian-travel.txt,” the dictionary will have an entry {..., ’aloha’: [’early-internet.dat’, ’hawaiian-travel.txt’], ...}.
'''  # noqa

path = './data_files'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.dat' in file:
            files.append(os.path.join(r, file))

words = {}
for f in files:
    with open(f, "r", encoding="ISO-8859-1") as f_handle:
        words_per_file = re.findall(r"\w+", str(f_handle.read()))
        for word in words_per_file:
            word = word.lower()
            if word in words.keys():
                if f not in words[word]:
                    words[word].append(f)
            else:
                words[word] = []
                words[word].append(f)

for w in words:
    print(w + " = " + str(words[w]))

with open("word_path_dictionary.pickle", "wb") as oFile:
    pickle.dump(words, oFile)
