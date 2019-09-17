import pickle

with open("word_path_dictionary.pickle", "rb") as iFile:
    object = pickle.load(iFile)

for (key, value) in object.items():
    print(key, value)
