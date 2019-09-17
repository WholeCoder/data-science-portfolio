import urllib.request
import sys
import re

"""Word Frequency Counter*Write a program that downloads a web page requested by the user and reports up to ten most frequently used words. The program should treat all words as case-insensitive. For the purpose of this exercise, assume that a word is described by the regular expression r"\w+"."""  # noqa


try:
    with urllib.request.urlopen("http://justinjackson.ca/words.html") as doc:
        html = doc.read()
        words = re.findall(r"\w+", str(html))
        freq = {}
        for word in words:
            word = word.lower()
            if word in freq.keys():
                freq[word] += 1
            else:
                freq[word] = 1
        line_number = 1
        for key, value in sorted(freq.items(), key=lambda item: item[1],reverse=True):
            if line_number == 11:
                break
            print(key + " = " + str(value))
            line_number += 1
except (RuntimeError, TypeError, NameError) as err:
    print("Could not open %s" % doc)
    print(err)


