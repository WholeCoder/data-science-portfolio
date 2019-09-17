from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib
from urllib.error import URLError

'''Broken Link Detector*Write a program that, given a URL of a web page, reports the names and destinations of broken links in the page. For the purpose of this exercise, a link is broken if an attempt to open it with urllib.request.urlopen fails.'''

#  Construct soup from a web document
#  Remember that urlopen() does not add "http://"! 

soup3 = BeautifulSoup(urlopen("http://www.deadlinkcity.com/"), features="html.parser")  # noqa

lnks = soup3.find_all("a")

for l in lnks:
    try:
        urllib.request.urlopen(l.get("href"))
    except URLError as E:
        print(E)
        print(str(l.get("href")) + " is a broken link!")
    except ValueError as V:
        pass
    #  print(l.get("href"))

#  print(lnks)
