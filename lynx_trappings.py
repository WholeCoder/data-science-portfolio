import os
import urllib.request
import pandas as pd
import numpy as np

if not os.path.exists('cache'):
    print("cache does not exist - creating it")
    os.mkdir('cache')

if not os.path.exists('cache/lynx.csv'):
    print("lynx.csv doesn't exist - downloading")
    url = 'http://vincentarelbundock.github.io/Rdatasets/csv/datasets/lynx.csv'
    urllib.request.urlretrieve(url, 'cache/lynx.csv')

if not os.path.exists('doc'):
    print("doc does not exist - creating it")
    os.mkdir('doc')

lynx = pd.read_csv("cache/lynx.csv", header=0)
#  print(lynx[(lynx["time"] >= 1820) & (lynx["time"] <= 1829)])
print(lynx.axes)

lynx['time'] = lynx['time'].apply(lambda x: (x // 10) * 10)

lynx = lynx.groupby(['time']).aggregate(np.sum)
#  lynx['time'] = lynx['time'].apply(lambda x: x * 10)

lynx = lynx.sort_values(by=['value'], ascending=False)

lynx = lynx[['value']]

print(lynx)
lynx.to_csv('doc/lynx_stats.csv')
