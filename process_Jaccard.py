import pickle


def J(A, B):
    denom = (len(A) + len(B) - len(A.intersection(B)))
    #  if denom == 0:
    #      return 0
    return len(A.intersection(B))/denom


with open('genres.pickle', 'rb') as f:
    data = pickle.load(f)

jaccardDict = {}

for genreA in data.keys():
    for genreB in data.keys():
        if genreA.strip() != genreB.strip():
            jaccardDict[(genreA, genreB)] = J(data[genreA], data[genreB])
            #  print("Comparing " + genreA + " to " + genreB + " J(A,B) = " + str(jaccardDict[(genreA, genreB)]))  # noqa

pickle.dump(jaccardDict, open("jaccard.pickle", "wb"))

removed_duplicates = {}
for jk in jaccardDict.keys():
    if jk not in removed_duplicates.keys() and (jk[1], jk[0]) not in removed_duplicates.keys():  # noqa
        removed_duplicates[jk] = jaccardDict[jk]

jaccardDict = removed_duplicates

sorted_jaccard = sorted(jaccardDict.items(), key=lambda kv: kv[1])

for sj in sorted_jaccard:
    print(str(sj[0]) + " = " + str(sj[1]))

print("\n\n Total number of genres = " + str(len(data.keys())))
