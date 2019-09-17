import pymysql
import sys
import pymongo as mongo

theTable = sys.argv[1]

conn = pymysql.connect(host="localhost", port=3306, user="rpierich", passwd="msGoogle&Boogle2", db="mysql_file_index")  # noqa

cur = conn.cursor()
describeStatement = "DESCRIBE " + theTable

n_rows = cur.execute(describeStatement)
columnDescriptorResults = list(cur.fetchall())
print("columnDescriptorResults == " + str(columnDescriptorResults))

selectClause = "SELECT "
for result in columnDescriptorResults:
    selectClause += result[0]+","
selectClause = selectClause[:-1] + " FROM " + theTable
#  print(selectClause)

selectStatement = selectClause

cur = conn.cursor()

n_rows = cur.execute(selectStatement)

results = list(cur.fetchall())
print("results == " + str(results))




client2 = mongo.MongoClient("localhost", 27017)

db = client2[theTable]
file_index = db[theTable]


for result in results:
    dct = {}
    i = 0
    for value in result:
        print("value = "+str(value))
        if columnDescriptorResults[i][1] == 'tinytext':
            dct[columnDescriptorResults[i][0]] = value
        elif columnDescriptorResults[i][1] == 'int(11)':
            dct[columnDescriptorResults[i][0]] = int(value)
        elif columnDescriptorResults[i][1] == 'timestamp':
            dct[columnDescriptorResults[i][0]] = str(value)
        i += 1
    print("dct == "+str(dct))
    file_index.insert_one(dct)
    print(result)

client2.close()
