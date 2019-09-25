from bs4 import BeautifulSoup
import pandas as pd

soup = BeautifulSoup(open("s_and_p_500.html"), features="html.parser")  # noqa

first = True
df_hash = {"Close": [], "Volume": []}
for tr in soup.find_all('tr'):
    if first:
        first = False
        continue
    if len(tr.find_all('td')) < 4:
        print("excluded == " + tr.get_text())
        continue
    df_hash["Close"].append(float(tr.find_all('td')[4].get_text().replace(',', '')))  # noqa
    df_hash["Volume"].append(float(tr.find_all('td')[6].get_text().replace(',', '')))  # noqa
    #  print(tr.find_all('td')[4].get_text() + " -> " + tr.find_all('td')[6].get_text())  # noqa

df = pd.DataFrame(df_hash)
print(df)
print(df.describe())
print(df.skew())
print(df.corr())
