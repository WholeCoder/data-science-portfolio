import nltk
import networkx as nx
from community import community_louvain
import community
from bs4 import BeautifulSoup
import os
from os import listdir
from os.path import isfile, join
from collections import Counter
from nltk.corpus import stopwords

#  nltk.download()


def get_tuple_counts(mypath):

    shake_soup = BeautifulSoup(open(mypath, encoding="ISO-8859-1"), features="html.parser") # noqa
    txt = shake_soup.get_text()
    lst_toked = nltk.word_tokenize(txt)
    lstemmer = nltk.LancasterStemmer()
    lst_toked_stemmed = [lstemmer.stem(w.lower()) for w in lst_toked if w not in stopwords.words("english") and w.isalnum()]# noqa
    cntr = Counter(lst_toked_stemmed)
    m_common = cntr.most_common()
    m_common_sorted = sorted(m_common, key=lambda tpl: tpl[1], reverse=True)

    frequency_denominator = sum([x[1] for x in m_common_sorted])

    G = nx.Graph()

    for tpl in m_common_sorted[0:10]:
        G.add_edge(mypath.split(os.sep)[1].split('.html')[0], tpl[0])
        G[mypath.split(os.sep)[1].split(".html")[0]][tpl[0]]["weight"] = tpl[1] / frequency_denominator # noqa
    return G


mypath = "shakespear_plays"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
grphs = []
for f in onlyfiles:
    grph = get_tuple_counts(join("shakespear_plays", f))

    #  for (u, v, wt) in grph.edges.data('weight'):
    #       print((u, v, wt))
    grphs.append(grph)
    #  print("-----------------------")
    #  print(grph)

c = grphs[0]
for i in range(len(grphs)):
    if i == 0:
        continue
    c = nx.compose(c, grphs[i])

partition = community_louvain.best_partition(c)
print("partition-----------------------")
print(partition)

com = community.modularity(partition, c)
print("community----------------------")
print(com)
