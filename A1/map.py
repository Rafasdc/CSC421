import numpy as np
from scipy.spatial import distance
from random import randint
from random import shuffle
from collections import deque
from utils import memoize
from utils import PriorityQueue


class MapProblem:
	def __init__(self, initial, goal, cities_distances, cities_locations, heuristic='e'):
		self.initial = initial
		self.goal = goal
		self.cities_distances=cities_distances
		self.cities_locations=cities_locations
		#Set default h to he
		self.h = self.h_e
		#change heuristic accordingly
		if heuristic == 'e':
			self.h = self.h_e
		elif heuristic == 'z':
			self.h = self.h_zero
		elif heuristic == 'm':
			self.h = self.h_m

	def goal_test(self, state):
		return state == self.goal

	def path_cost(self,city1,city2):
		return self.cities_distances[city1][city2]

	def actions(self, state):
		#The possible actions is go to any city that has a path 
		#in one hop. 
		possible_actions = list(cities_distances[state].keys())
		return possible_actions

		
	def result(self,state,action):
		#result of action would be new city based on current state
		new_state = cities_distances[state][action]
		return new_state

	def h_e(self,node):
		return round(distance.euclidean(self.cities_locations[node.state],self.cities_locations[self.goal]),2)

	def h_zero(self,node):
		return 0

	def h_m(self,node):
		return round(distance.cityblock(self.cities_locations[node.state],self.cities_locations[self.goal]),2)


class Graph:

	def __init__(self, cities_distances=None):
		self.cities_distances = cities_distances or {}
		#self.make_undirected()

	def make_undirected(self):
		for city in self.cities_distances:
			for (toCity, dist) in self.cities_distances[city].items():
				self.cities_distances.setdefault(toCity,{})[city] = dist

class Node:

	def __init__(self, state, parent=None, action=None, path_cost=0):
		self.state=state
		self.parent=parent
		self.action=action
		self.path_cost=path_cost
		self.depth=0
		if parent:
			self.depth = parent.depth+1

	def __lt__(self,node):
		return self.state < node.state

	def expand(self,problem):
		#print(self.state)
		#print(list(problem.cities_distances[self.state].keys()))
		return [self.child_node(problem,action) for action in problem.actions(self.state)]
		#keys = list(cities_distances[city].keys())
		#return keys

	def child_node(self,problem,action):
		#next_node = problem.cities_distances[self.state]
		#print(self.state)
		#print(action)
		return Node(action,self,None,problem.path_cost(self.state,action))


def generate_map():

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
		#print(distances)
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
	return (cities_locations,cities_distances)

'''
Makes unidrected graph
Moved to Graph Class
'''
'''
for city in cities_locations:
	for (toCity, dist) in cities_distances[city].items():
		cities_distances.setdefault(toCity,{})[city] = dist
print(cities_distances)
'''

#---------- Uniformed Search ------------

def breadth_first_search(problem):
	node = Node(problem.initial)
	if problem.goal_test(node.state):
		return node
	frontier = deque([node])
	explored = set()
	while frontier:
		node = frontier.popleft()
		explored.add(node.state)
		for child in node.expand(problem):
			if child.state not in explored and child not in frontier:
				if problem.goal_test(child.state):
					return child
				frontier.append(child)
	return None

def depth_first_search(problem):
	frontier = [(Node(problem.initial))]
	explored = set()
	while frontier:
		node = frontier.pop()
		if problem.goal_test(node.state):
			return node
		explored.add(node.state)
		frontier.extend(child for child in node.expand(problem)
                        if child.state not in explored and
                        child not in frontier)
	return None

def recursive_dls(node,problem,limit):
	if problem.goal_test(node.state):
		return node
	elif limit == 0:
		return 0
	else:
		cutoff_occured = False
		for child in node.expand(problem):
			result = recursive_dls(child,problem,limit-1)
			if result == 0:
				cutoff_occured = True
			elif result is not None:
				return result
		return 0 if cutoff_occured else None

def depth_limited_search(problem,limit):
	return recursive_dls(Node(problem.initial),problem,limit)

def iterative_deepening_search(problem):
	for depth in range(13):
		result = depth_limited_search(problem,depth)
		if result != 0:
			return result

#-------------- End Uniformed Search -----------------


#-------------- Informed search ----------------------

def greedy_best_first_search(problem):
	h = memoize(problem.h, 'h')
	node = Node(problem.initial)
	if problem.goal_test(node.state):
		return node
	frontier = PriorityQueue('min', h)
	frontier.append(node)
	explored = set()
	while frontier:
		node = frontier.pop()
		if problem.goal_test(node.state):
			return node
		explored.add(node.state)
		for child in node.expand(problem):
			if child.state not in explored and child not in frontier:
				frontier.append(child)
			elif child in frontier:
				incumbent = frontier[child]
				if h(child) < h(incumbent):
					del frontier[incumbent]
					frontier.append(child)
	return None

def a_star_search(problem):
	return None

#-------------- End Informed Search -----------------

cities_locations, cities_distances = generate_map()
#print(cities_distances)
random_map = Graph(cities_distances)
#print(random_map.cities_distances)

for i in range(100):
	start = randint(65,90)
	goal = randint(65,90)

	print("Attempt solve from " + chr(start) + " to " + chr(goal))

	cities_locations, cities_distances = generate_map()

	random_map = Graph(cities_distances)
	#print(random_map.cities_distances)

	problem = MapProblem(chr(start),chr(goal),cities_distances,cities_locations)

	result = breadth_first_search(problem)
	#print(result)

	node, path_back = result, []
	while node:
		path_back.append(node.state)
		node = node.parent

	print(list(reversed(path_back)))

	result_b = depth_first_search(problem)

	node, path_back = result_b, []
	while node:
		path_back.append(node.state)
		node = node.parent

	print(list(reversed(path_back)))

	result_i = iterative_deepening_search(problem)

	node, path_back = result_i, []
	while node:
		path_back.append(node.state)
		node = node.parent

	print(list(reversed(path_back)))

	result_gb = greedy_best_first_search(problem)

	node, path_back = result_gb, []
	while node:
		path_back.append(node.state)
		node = node.parent
	print(list(reversed(path_back)))





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

