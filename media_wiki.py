import mwclient
import pprint

site = mwclient.Site('en.wikipedia.org')

#result = site.api(action='query', prop='coordinates', titles='Oslo|Copenhagen')  # noqa
result = site.api(action='query',revids='347819%7C5487%7C548945',format='jsonfm',formatversion='2')  # noqa
pprint.pprint(result)

page = site.pages[u'Leipäjuusto']

#  print(page.text())

cats = [x for x in page.categories()]

#  for c in cats:
#   print(c)
