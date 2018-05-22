import numpy as np
from scipy.spatial import distance
from random import randint
from random import shuffle
from collections import deque


class MapProblem:
	def __init__(self, initial, goal, cities_distances):
		self.initial = 'A'
		self.goal = 'P'
		self.cities_distances=cities_distances

	def goal_test(self, state):
		return state == self.goal

	def path_cost(self,city1,city2):
		return self.cities_distances[city1][city2]

class Graph:

	def __init__(self, cities_distances=None):
		self.cities_distances = cities_distances or {}
		self.make_undirected()

	def make_undirected(self):
		for city in self.cities_distances:
			for (toCity, dist) in self.cities_distances[city].items():
				self.cities_distances.setdefault(toCity,{})[city] = dist


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

#print(cities_locations)
#print(cities_locations['A'])

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
#print(cities_distances)

'''
Randomly decide between having 1 or 4 paths between cities
and randomly choose the paths
'''
for city in cities_locations:
	paths = randint(1,4)
	keys = list(cities_distances[city].keys())
	shuffle(keys)
	for i in range(len(keys)-paths):
		cities_distances[city].pop(keys[i],None)
#print(cities_distances)


'''
Makes unidrected graph
'''

for city in cities_locations:
	for (toCity, dist) in cities_distances[city].items():
		cities_distances.setdefault(toCity,{})[city] = dist
print(cities_distances)



goal = 'B'
initial_state = 'J'

cur_state = initial_state

#breadth_first_search(cur_state)


if cur_state == goal:
	print("DONE")
frontier = deque(cur_state)
explored = set()
while frontier:
	done = 0
	cur_state = frontier.popleft()
	explored.add(cur_state)
	for city in cities_distances[cur_state]:
		if city not in explored and city not in frontier:
			print(city)
			if city == goal:
				print("DONE")
				done = 1
			frontier.append(city)
	if done == 1:
		break

random_map = Graph(cities_distances)



'''
# ---- Start Problem ------

class Problem(object):

	def __init__(self, initial, goal=None):
		self.initial = 'A'
		self.goal = 'P'

	def goal_test(self, state):
		return state = self.goal

	def path_cost(self,cities_distances,city1,city2):
		return cities_distances[city1][city2]

# ----- End Problem -------


class Node:

	def __init__(self, state, parent=None, action=None, path_cost=0):
		self.state=state
		self.parent=parent
		self.action=action
		self.path_cost=path_cost
		self.depth=0
		if parent:
			self.depth = parent.depth+1

	def expand(self,problem):
		keys = list(cities_distances[city].keys())
		return keys

'''

'''

class Map:

	def __init__ (self, cities=None):
		self.cities = cities or {}

	def make_undirected(self):
		for i in list(self.cities.keys()):
			for (j, dist) in self.cities[a].items():
				self.
'''

