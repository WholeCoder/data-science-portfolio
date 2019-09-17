import csv
import numpy as np
import math

with open("hd2017.csv") as infile:
    data = list(csv.reader(infile))

institution_name_index = data[0].index("INSTNM")
longitude_index = data[0].index("LONGITUD")
latitude_index = data[0].index("LATITUDE")

name_ray = []
longitude_ray = []
latitude_ray = []

for row in data[1:]:
    name_ray.append(row[institution_name_index])
    longitude_ray.append(float(row[longitude_index]))
    latitude_ray.append(float(row[latitude_index]))

longitude_ray = np.array(longitude_ray)
latitude_ray = np.array(latitude_ray)

print("longitude mean = " + str(longitude_ray.mean()))
print("latitude mean = " + str(latitude_ray.mean()))

distance = []
for i, lng in enumerate(longitude_ray):
    distance.append((i, math.sqrt((lng - longitude_ray.mean())**2 + (latitude_ray[i] - latitude_ray.mean())**2)))  # noqa

#  distance = np.array(distance)
distance = sorted(distance, key=lambda dt: dt[1])
for d in distance[0:10]:
    print(name_ray[d[0]] + " = " + str(d[1]))

#  print(name_ray)
