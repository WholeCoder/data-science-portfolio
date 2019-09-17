import nltk

wn = nltk.corpus.wordnet
#  nltk.download()

sm = [simxy.definition() for simxy in max(
    (x.path_similarity(y), x, y)
        for x in wn.synsets('cat')
        for y in wn.synsets('dog')
        if x.path_similarity(y)
    )[1:]]

print(sm)
