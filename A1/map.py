import numpy as np
from scipy.spatial import distance
from random import randint
from random import shuffle

'''
Generate random location for Cities in a 100x100 grid
'''

cities_locations = dict()
curr_city = ord('A')

seen=set()
x, y = randint(0,99), randint(0,99)
cities_locations[chr(curr_city)] = (x,y)
for i in range (26):
	seen.add((x,y))
	x, y = randint(0,99), randint(0,99)
	while (x,y) in seen:
		x, y = randint(0,99), randint(0,99)
	cities_locations[chr(curr_city)] = (x,y)
	curr_city += 1

print(cities_locations)
print(cities_locations['A'])

'''
Calculate Euclidean Distances between cities and keep 5 closest
'''
distances = (['city',999], ['city',999], ['city',999], ['city',999], ['city',999])
#print(distance.euclidean(cities_locations['A'], cities_locations['B']))
cities_distances=dict()
for city1 in cities_locations:
	cities_distances[city1] = dict()
	for city2 in cities_locations:
			for i in range(len(distances)):
				euclidean = distance.euclidean(cities_locations[city1],cities_locations[city2])
				if euclidean == 0:
					break
				if euclidean < distances[i][1]:
					distances[i][0] = city2
					distances[i][1] = round(euclidean,2)
					break
	print(distances)
	for i in range(len(distances)):
		cities_distances[city1][distances[i][0]] = distances[i][1]
	distances = (['city',999], ['city',999], ['city',999], ['city',999], ['city',999])
print(cities_distances)

'''
Randomly decide between having 1 or 4 paths between cities
and randomly choose the paths
'''
for city in cities_locations:
	paths = randint(1,4)
	print(paths)
	keys = list(cities_distances[city].keys())
	shuffle(keys)
	print(keys)
	for i in range(len(keys)-paths):
		cities_distances[city].pop(keys[i],None)
print(cities_distances)






'''

class Map:

	def __init__ (self, cities=None):
		self.cities = cities or {}

'''