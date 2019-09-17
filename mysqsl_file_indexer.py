import pymysql
import sys
from nltk.tokenize import WordPunctTokenizer
import nltk

nltk.download('averaged_perceptron_tagger')

theFile = sys.argv[1]

with open(theFile, mode="r") as f:
    file_contents = f.read()

word_punct = WordPunctTokenizer()
words = word_punct.tokenize(file_contents)
words_with_pos = nltk.pos_tag(words)

conn = pymysql.connect(host="localhost", port=3306, user="rpierich", passwd="msGoogle&Boogle2", db="mysql_file_index")  # noqa

insertStatement = '''
    INSERT INTO file_index (word, ordinal_number, pos_marker) VALUES (%s, %s, %s)
'''  # noqa

ordinal_number = 1

try:
    with conn.cursor() as cursor:
        for word_tuple in words_with_pos:
            tup = (word_tuple[0], ordinal_number, word_tuple[1])
            print(tup)
            cursor.execute(insertStatement, tup)  # noqa
            ordinal_number += 1
    conn.commit()
finally:
    conn.close()
