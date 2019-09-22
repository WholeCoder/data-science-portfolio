#  import pandas as pd
from bs4 import BeautifulSoup
import re
import networkx as nx
import community

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

    cities = {}
    if tds[5].find('div') is not None:
        txt = tds[5].find('div').find_all('div')[1].get_text().replace('\xa0', ' ').strip()  # noqa
        #  ['Russia: 241 km (150 mi) Georgia: 141 km (88 mi)']
        txt = re.sub(r'\[.*\]', '', txt)
        while txt.strip() != '':
            txt = txt.replace(',', '')
            #  print('txt = ' + txt)
            #  print(txt)
            m = re.search("([\)\(\w\' ]+): [0-9.]+ km \(([0-9.]+) mi\)", txt)
            if m is None:
                break
            country_name = m.group(1)
            #  print("m.group(1) == " + country_name)
            country_miles = m.group(2)
            #  print("m.group(2) == " + country_miles)
            cities[country_name] = country_miles
            if m.group(0) in txt:
                txt = txt.replace(m.group(0), '').strip()
    else:
        pass
        #  print("NoneType found")
    #  lst.append(txt)
    #  lst.append(tds[5].find('div').find_all('div')[1].get_text())
    #   if len(tds[5]) > 0 and len(tds[5].find('div').find_all('div')) > 0:
    #      txt = tds[5].find('div').find_all('div')[1].get_text()
    #      lst.append([txt])

    #  for bord_cont in tds[5].find('div'):
    #    lst.append(bord_cont.find('div')[0].get_text())

    land_border_hash["Land border neighbours<br>and border length"].append(cities)  # noqa
    #  td5 = tds[5]
    #  land_border_hash["Land border neighbours<br>and border length"].append(td5)  # noqa
G = nx.Graph()

#  for k in land_border_hash.keys():
#    print(k + " -> " + str(land_border_hash[k]))
#    print("\n\n\n---------------------------------------------- length == " + str(len(land_border_hash[k])))  # noqa
for x in land_border_hash["Country or territory"]:
    #  print(x)
    G.add_node(x)

print('edges--------------------------------')

for i in range(len(land_border_hash["Land border neighbours<br>and border length"])):  # noqa
    country = land_border_hash["Country or territory"][i]
    if "length" not in G.node[country]:
        G.node[country]["length"] = 0.0
    for k in land_border_hash["Land border neighbours<br>and border length"][i].keys():  # noqa)
        G.add_edge(country, k)
        ln = float(land_border_hash["Land border neighbours<br>and border length"][i][k])  # noqa
        #  G[country][k]['weight'] = ln  # noqa
        G.node[country]["length"] += ln
for n in G.edges:
    print(n)
print(G)
#  df = pd.DataFrame(land_border_has

part = community.best_partition(G)
print(community.modularity(part, G))

with open("borders-1.graphml", "wb") as graph:
    nx.write_graphml(G, graph)
