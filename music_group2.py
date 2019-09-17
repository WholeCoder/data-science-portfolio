#!/usr/bin/python3
import pickle

"""
    get_categories.py

    MediaWiki API Demos
    Demo of `Categories` module: Get categories associated with a page.

    MIT License
"""

import requests
import pprint

#  api.php?action=query&list=categorymembers&cmtitle=Category:Wikipedia&cmtype=subcat
'''PARAMS = {
    "action": "query",
    "list": "categorymembers",
    "cmtitle": "Category:Musical subgenres by genre",
    "cmtype": "subcat",
    "format": "json",
    "cmlimit": 100
}'''

#  List of popular music genres

PARAMS = {
    "action": "parse",
    "page": "British rock music",
    "format": "json",
    #  "list": "categorymembers",
    #  "cmtitle": "Category:Rock music",
}
#  PARAMS = {
#    "action": "query",
#    "format": "json",
#    "prop": "categories",
#    "titles": "Category:Rock music"
#  }

wDict = {}
artistDict = {}

current_set_of_genres = set()

genreDict = {}

def print_links(level, pg):
    global artistDict
    global wDict
    global current_set_of_genres
    
    if pg in artistDict.keys():
        print("pg already in artistDict() print_links - found " + pg + "in keys()")
        return
    print("found link - in print_links() == "+level*"  "+str(level)+" "+pg)
    global wDict
    global current_set_of_genres

    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
        "action": "query",
        "titles": pg,
        "format": "json",
        "prop": "links",
        "pllimit": "500"
        #  "list": "categorymembers",
        #  "cmtitle": "Category:Rock music",
    }
    try:
        R = S.get(url=URL, params=PARAMS)
        DATA2 = R.json()
        R.close()
        # if pg.startswith("List of"):
            # print(level*"  " + pg)

        #  pprint.pprint(DATA2)
        #  exit(0)
        pageid = list(DATA2["query"]["pages"].keys())[0]
        PAGES = DATA2["query"]["pages"][pageid]["links"]
        #  pprint.pprint(DATA2["query"])
        for page in PAGES:
            if page['ns'] == 0:
                #  print(level*" " + page['title'])
                if page['title'].startswith('List of'):
                    print_links(level + 1, page['title'])
                    if page['title'] not in artistDict.keys():
                        artistDict[page['title']] = set()
                    artistDict[page['title']].update(current_set_of_genres)
    except UnicodeError as k:
        print("KeyError == " + str(k))
#  R = S.get(url=URL, params=PARAMS)
#  DATA = R.json()

#  pprint.pprint(DATA)

#  exit(0)


level_limiter = 1


def get_sub_categories(level, ct):
    global level_limiter
    global artistDict
    global wDict
    global current_set_of_genres

    if ct.strip().startswith("List of ") and ct.strip().split("List of ")[1] in artistDict.keys():  # noqa
        return
    elif ct.strip().startswith("Category:") and ct.strip().split("Category:")[1] in artistDict.keys():  # noqa
        return

    print("found in get_sub_categories() - level  "+str(level)+" "+ct)

    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {
             "action": "query",
             "cmtitle": ct,
             "cmlimit": "500",
             "list": "categorymembers",
             "format": "json"
             }
    #  if not ct.startswith("Category:"):
    #      print_links(level+1, ct)
    #      return
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    R.close()
    #  pprint.pprint(DATA)
    #if level > level_limiter:
    #    return
    #level_limiter += 1

    PAGES = DATA['query']['categorymembers']
    if len(PAGES) > 0:
        for page in PAGES:
            if page['ns'] != 14:
                for genre in current_set_of_genres:
                    if genre not in genreDict.keys():
                        genreDict[genre] = set()
                    if page['title'].strip() not in genreDict[genre]:
                        genreDict[genre].add(page['title'].strip())
                if page['title'] in artistDict.keys():
                    artistDict[page['title']].update(current_set_of_genres.copy())  # noqa
                    print("a page " + level*"   " + page['title'] + str(artistDict[page['title']]))  # noqa
                else:
                    artistDict[page['title']] = current_set_of_genres.copy()
                    print("a page " + level*"  " + page['title'] + str(artistDict[page['title']]))  # noqa
            elif page['ns'] == 14:
                current_set_of_genres.add(page['title'].split(':')[1].strip())
            if page['ns'] == 14:
                #  print(level*"  " + page['title'])
                if page['title'].startswith("Category:"):
                    name = page['title'].split(":")[1]
                elif page['title'].startswith("List of "):
                    name = page['title'].split("List of ")[1]
                if name.strip() in wDict.keys():
                    return
                else:
                    wDict[name] = name
                current_set_of_genres = current_set_of_genres.copy()
                current_set_of_genres.add(name.strip())
                print("    Added to set of groupos == "+str(current_set_of_genres))  # noqa
                get_sub_categories(level+1, page['title'])
                current_set_of_genres = current_set_of_genres.copy()
                current_set_of_genres.discard(name)
                print("     Removed to set of groupos == "+str(current_set_of_genres))  # noqa
            elif page['ns'] == 10:
                if page['title'].strip() not in artistDict.keys():
                    artistDict[page['title']] = set()
                current_set_of_genres = current_set_of_genres.copy()
                artistDict[page['title']] = current_set_of_genres #  .update(current_set_of_genres)
                 
#                if page['title'].startswith('List of '):
#                    if page['title'] in wDict.keys():
#                        return
#                    else:
#                        wDict[page['title'].split("List of ")[1].strip()] = page['title'].split("List of ")[1].strip()   # noqa
#                        print_links(level+1, page['title'])



current_set_of_genres.add("British rock music groups by genre")
current_set_of_genres = current_set_of_genres.copy()
get_sub_categories(0, "Category:British rock music groups by genre")

print(artistDict.keys())

pickle.dump(artistDict, open("artists.pickle", "wb"))
#  print_links(0, "List of alternative metal artists")
pickle.dump(genreDict, open("genres.pickle", "wb"))

def get_categories(ct):
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    PARAMS = {"action": "query",
              "cmtitle": ct,
              "cmlimit": "20",
              "list": "categorymembers",
              "format": "json"}

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()

    PAGES = DATA['query']['categorymembers']

    #  for page in PAGES:
        #  print(page['title'])


#  get_categories("Category:Band (rock and pop)")
