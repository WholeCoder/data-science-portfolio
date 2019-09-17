import pandas as pd
from bs4 import BeautifulSoup

alcohol_soup = BeautifulSoup(open("List_of_countries_by_alcohol_consumption_per_capita-Wikipedia.html"), features="html.parser")  # noqa

alcohol_by_gdp_data_hash = {}
for th in alcohol_soup.find('thead').find_all('th'):
    alcohol_by_gdp_data_hash[th.get_text().strip()] = []

#  df = pd.DataFrame(columns=alcohol_by_gdp_cols)
for tr in alcohol_soup.find('tbody').find_all('tr'):
    for z in zip(alcohol_by_gdp_data_hash.keys(), tr.find_all('td')):
        alcohol_by_gdp_data_hash[z[0]].append(z[1].get_text().strip())
df = pd.DataFrame(alcohol_by_gdp_data_hash)

print(df)

countries_by_gdp_soup = BeautifulSoup(open("List_of_countries_by_GDP_(PPP)_per_capita-Wikipedia.html"), features="html.parser")  # noqa

countries_by_gdp_hash = {}
for th in countries_by_gdp_soup.find('thead').find_all('th'):
    countries_by_gdp_hash[th.get_text().strip()] = []

for tr in countries_by_gdp_soup.find_all('table')[1].find('table').find('tbody').find_all('tr'):  # noqa
    for z in zip(countries_by_gdp_hash.keys(), tr.find_all('td')):
        countries_by_gdp_hash[z[0]].append(z[1].get_text().strip())

countries_by_gdp_frame = pd.DataFrame(countries_by_gdp_hash)

print(countries_by_gdp_frame)

merged_df = df.merge(countries_by_gdp_frame, left_on='Country', right_on='Country/Territory')  # noqa

merged_df['Int$'] = merged_df['Int$'].str.replace(',', '').replace('n/a', '0').astype(float)  # noqa

merged_df['Total'] = merged_df['Total'].str.replace(',', '').replace('n/a', '0').astype(float)  # noqa


def ab_mean(x):
    if x > merged_df['Int$'].mean():
        return 'Above'
    return 'Lower'


def ab_alco_mean(x):
    if x > merged_df['Total'].mean():
        return 'Above'
    return 'Lower'


merged_df['AB Mean Int $'] = merged_df['Int$'].apply(ab_mean)
merged_df['AB Mean Total Alco Consumption'] = merged_df['Total'].apply(ab_alco_mean)  # noqa

merged_df = merged_df[['AB Mean Int $', 'AB Mean Total Alco Consumption']]
merged_df = merged_df.groupby(["AB Mean Int $", "AB Mean Total Alco Consumption"]).size() # noqa
print(merged_df)# noqa
#  gb_frame = merged_df.groupby(['AB Mean Int $', 'AB Mean Total Alco Consumption']).count()  # noqa
#  print(gb_frame.describe())
