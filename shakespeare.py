import nltk
import networkx as nx
from bs4 import BeautifulSoup
from os import listdir
from os.path import isfile, join
from collections import Counter
from nltk.corpus import stopwords

#  nltk.download()


def get_tuple_counts(mypath):

    shake_soup = BeautifulSoup(open("shakespear_plays/All's Well That Ends Well: Entire Play.html", encoding="ISO-8859-1"), features="html.parser") # noqa
    txt = shake_soup.get_text()
    lst_toked = nltk.word_tokenize(txt)
    lstemmer = nltk.LancasterStemmer()
    lst_toked_stemmed = [lstemmer.stem(w.lower()) for w in lst_toked if w not in stopwords.words("english") and w.isalnum()]# noqa
    cntr = Counter(lst_toked_stemmed)
    m_common = cntr.most_common()
    m_common_sorted = sorted(m_common, key=lambda tpl: tpl[1], reverse=True)

    return m_common_sorted


mypath = "shakespear_plays"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
graph_list_tuples = []
for f in onlyfiles:
    tp_list = get_tuple_counts(join("shakespear_plays", f))
    graph_list_tuples.append(tp_list)

for gl in graph_list_tuples:
    print("-------------------------")
    print(gl)
