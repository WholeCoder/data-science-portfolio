import mwclient
import re

site = mwclient.Site('en.wikipedia.org')

#result = site.api(action='query', prop='coordinates', titles='Oslo|Copenhagen')  # noqa
#result = site.api(action='query',revids='347819%7C5487%7C548945',format='jsonfm',formatversion='2')  # noqa
#  pprint.pprint(result)

page = site.pages[u'Music genre']

print(page.categories())

exit(0)
found_genres = re.findall(r"={2,3}([\w\s\w/&]{1,})={2,3}", page.text())

print("found_genres == " + str(found_genres))


def extract_genres(r2):
    return r2.strip()


print("len == " + str(len(found_genres)))
found_genres = set(map(extract_genres, found_genres))

print("found_genres == " + str(found_genres))

found_genres -= {"Traditional and folk music", "Religious music", "Psychology of music preference", "Art music", "Individual and situational influences", "Gender", "See also", "Further reading", "Social influences on music selection", "Popular music", "Age", "Automatic categorization", "References"}  # noqa

for f in found_genres:
    print(f)

page = site.pages[u'Rock music']
page = site.pages[u'blues rock']
page = site.pages[u'punk blues']
page = site.pages[u'List of punk blues musicians and bands']


txt = page.text()
#txt = txt[1].split("| subgenres = * ")[1]
#  print(txt)
found_rock = re.findall(r"\[\[([\w\s\W/&]{1,}?)\]\]", str(txt))

for f in found_rock:
    print("f == " + f)

print("txt == " + str(txt))
genres = [x for x in page.categories()]

#  for c in genres:
#    print(c.name)
