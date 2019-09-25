import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

ca_pop_list = []
california_pop_soup = BeautifulSoup(open("CPS_for_CA.html"), features="html.parser")  # noqa
for tr in california_pop_soup.find_all('tr'):
    print(tr.find('th').get_text())
    print(tr.find('td').get_text())
    ca_pop_list.append(float(tr.find('td').get_text().replace(',', '')))
ca_pop_list = np.array(ca_pop_list)

tot_consump_list = []
total_pop_soup = BeautifulSoup(open("CPS_population_per_year.html"), features="html.parser")  # noqa
for tr in total_pop_soup.find_all('tr'):
    print(tr.find('th').get_text())
    print(tr.find('td').get_text())
    tot_consump_list.append(float(tr.find('td').get_text().replace(',', '')))  # noqa
tot_consump_list = np.array(tot_consump_list)

# Select the right data
years = range(2011, 2018)
states = ("New Hampshire", "Colorado", "Utah")

# Select a good-looking style
plt.xkcd()
matplotlib.style.use("ggplot")

# Plot the charts

ydata = tot_consump_list
plt.plot(years, ydata, "-o")
# Add annotations with arrows
plt.annotate(s="Peak", xy=(ydata.argmax(), ydata.max()),
             xytext=(7, 400_000_000))
ydata = ca_pop_list
plt.plot(years, ydata, "-o")
# Add annotations with arrows
plt.annotate(s="Peak", xy=(ydata.argmax(), ydata.max()),
             xytext=(7, 400_000_000))

#
# Add labels and legends
#  plt.ylabel(BEVERAGE + " consumption")
plt.title("And now in xkcd...")
#plt.legend(states)

plt.savefig("pyplot-legend-xkcd.pdf")
