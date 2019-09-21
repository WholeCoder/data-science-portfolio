#  import pandas as pd
from bs4 import BeautifulSoup

land_border_soup = BeautifulSoup(open("List_of_countries_and_land_borders.htm"), features="html.parser")  # noqa

land_border_hash = {}
land_border_hash["Country or territory"] = []
land_border_hash["Land border neighbours<br>and border length"] = []


#  df = pd.DataFrame(columns=alcohol_by_gdp_cols)
not_found = True

for tr in land_border_soup.find_all('tr'):
    tds = tr.find_all("td")
    if not_found:
        print(str(len(tds)))
        if len(tds) > 0:
            print(str(tds[0].find('a').get_text()))
        if len(tds) > 0 and tds[0].find('a').get_text() == 'Abkhazia':
            not_found = False
            print("found counry")
        else:
            continue
    if len(tds) == 0:
        continue
    if tds[0].find('a').get_text() == 'Total':
        break
    land_border_hash["Country or territory"].append(tds[0].find('a').get_text()) # noqa

    lst = []
    if tds[5].find('div') is not None:
        txt = tds[5].find('div').find_all('div')[1].get_text().replace('\xa0', ' ').strip()  # noqa
        print(txt)
    else:
        print("NoneType found")
    lst.append(txt)
    #  lst.append(tds[5].find('div').find_all('div')[1].get_text())
    #   if len(tds[5]) > 0 and len(tds[5].find('div').find_all('div')) > 0:
    #      txt = tds[5].find('div').find_all('div')[1].get_text()
    #      lst.append([txt])

    #  for bord_cont in tds[5].find('div'):
    #    lst.append(bord_cont.find('div')[0].get_text())

    land_border_hash["Land border neighbours<br>and border length"].append(lst)  # noqa
    #  td5 = tds[5]
    #  land_border_hash["Land border neighbours<br>and border length"].append(td5)  # noqa

for k in land_border_hash.keys():
    print(k + " -> " + str(land_border_hash[k]))
    print("\n\n\n----------------------------------------------")
#  df = pd.DataFrame(land_border_hash)
