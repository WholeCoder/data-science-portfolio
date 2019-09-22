from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt


abbrv_soup = BeautifulSoup(open("state_abbreviations.html"), features="html.parser")  # noqa 
trs = abbrv_soup.find('table', {"class": "f"}).find_all('tr')

first_initial_list = []
for tr in trs[2:]:
    #  print(tr.get_text())
    first_initial_list.append([tr.find_all('td')[0].get_text()[0:1], tr.find_all('td')[0].get_text()]) # noqa

#  for ele in first_initial_list:
#      print(ele[0] + " -> " + ele[1])

df = pd.DataFrame(first_initial_list, columns=["Initial", "State Name"])

print(df.groupby(["Initial"]).groups.keys())
state_name_list_lables = []
count_of_initials = []
for g, data in df.groupby('Initial'):
    print("     " + g)
    txt = ""
    count = 0
    for d in data['State Name']:
        txt += d + "\n"
        print(d)
        count += 1
    state_name_list_lables.append(txt)
    count_of_initials.append(count)



#  Pie chart, where the slices will be ordered and plotted counter-clockwise: # noqa
labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes = count_of_initials  #  [15, 30, 45, 10]
explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=state_name_list_lables, autopct='%1.1f%%', shadow=True, startangle=90)  # noqa
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle. # noqa

plt.show()
