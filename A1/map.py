import numpy as np
from scipy.spatial import distance
from random import randint
from random import shuffle
from collections import deque
from utils import memoize
from utils import PriorityQueue
import time

ids_visited = 0
ids_generated = 0

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

	#Used for A* Search computes h(n) + g(n)
	def h_g(self,node):
		return (self.h(node) + node.path_cost)

class Graph:

	def __init__(self, cities_distances=None,undirected=False):
		self.cities_distances = cities_distances or {}
		if undirected:
			self.make_undirected()

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


def generate_map(report_paths=False):

	'''
	Generate random location for Cities in a 100x100 grid
	'''
	total_paths = 0

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
		total_paths += paths
		keys = list(cities_distances[city].keys())
		shuffle(keys)
		for i in range(len(keys)-paths):
			cities_distances[city].pop(keys[i],None)
	#print(cities_distances)
	if report_paths:
		return (cities_locations,cities_distances,total_paths)
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

def breadth_first_search(problem,stats=False):
	node = Node(problem.initial)
	explored = set()
	nodes_generated = 1 #the initial state
	if problem.goal_test(node.state):
		if stats:
			return (node,explored,nodes_generated)
		return node
	frontier = deque([node])
	while frontier:
		node = frontier.popleft()
		explored.add(node.state)
		for child in node.expand(problem):
			nodes_generated+= 1
			if child.state not in explored and child not in frontier:
				if problem.goal_test(child.state):
					if stats:
						return (child,explored,nodes_generated)
					return child
				frontier.append(child)
	return None

def depth_first_search(problem,stats=False):
	frontier = [(Node(problem.initial))]
	explored = set()
	nodes_generated = 1
	while frontier:
		node = frontier.pop()
		if problem.goal_test(node.state):
			if stats:
				return (node,explored,nodes_generated)
			return node
		explored.add(node.state)
		for child in node.expand(problem):
			nodes_generated+=1
		frontier.extend(child for child in node.expand(problem)
                       if child.state not in explored and
                       child not in frontier)
	return None

def recursive_dls(node,problem,limit):
	global ids_visited
	global ids_generated
	if problem.goal_test(node.state):
		ids_visited+=1
		return node
	elif limit == 0:
		return 0
	else:
		cutoff_occured = False
		for child in node.expand(problem):
			ids_generated += 1
			result = recursive_dls(child,problem,limit-1)
			if result == 0:
				cutoff_occured = True
			elif result is not None:
				ids_visited+=1
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

def greedy_best_first_search(problem,stats=False):
	h = memoize(problem.h, 'h')
	node = Node(problem.initial)
	nodes_generated = 1
	explored = set()
	if problem.goal_test(node.state):
		if stats:
			return (node,explored,nodes_generated)
		return node
	frontier = PriorityQueue('min', h)
	frontier.append(node)
	while frontier:
		node = frontier.pop()
		if problem.goal_test(node.state):
			if stats:
				return (node,explored,nodes_generated)
			return node
		explored.add(node.state)
		for child in node.expand(problem):
			nodes_generated += 1
			if child.state not in explored and child not in frontier:
				frontier.append(child)
			elif child in frontier:
				incumbent = frontier[child]
				if h(child) < h(incumbent):
					del frontier[incumbent]
					frontier.append(child)
	return None

'''
Same algorithm as GBFS, with the difference that uses the
h_g function in the problem class instead of h
h_g adds the path cost to the selected heuristic
'''
def a_star_search(problem,stats=False):
	h = memoize(problem.h_g, 'h')
	node = Node(problem.initial)
	nodes_generated = 1
	explored = set()
	if problem.goal_test(node.state):
		if stats:
			return (node,explored,nodes_generated)
		return node
	frontier = PriorityQueue('min', h)
	frontier.append(node)
	while frontier:
		node = frontier.pop()
		if problem.goal_test(node.state):
			if stats:
				return (node,explored,nodes_generated)
			return node
		explored.add(node.state)
		for child in node.expand(problem):
			nodes_generated += 1
			if child.state not in explored and child not in frontier:
				frontier.append(child)
			elif child in frontier:
				incumbent = frontier[child]
				if h(child) < h(incumbent):
					del frontier[incumbent]
					frontier.append(child)
	return None

#-------------- End Informed Search -----------------


#------------- Experimentation Starts ----------------

'''
#------Map branches test for Question 2 -----------
paths_10 = []
for i in range(10):
	_,_,total_paths = generate_map(True)
	paths_10.append(total_paths)
print(paths_10)

paths_100 = []
for j in range(100):
	_,_,total_paths = generate_map(True)
	paths_100.append(total_paths)
print(paths_100)

paths_1000 = []
for k in range(1000):
	_,_,total_paths = generate_map(True)
	paths_1000.append(total_paths)
print(paths_1000)

print("Average Number of paths for 10 iterations ")
print(np.mean(paths_10))
print("Average Number of paths for 100 iterations ")
print(np.mean(paths_100))
print("Average Number of paths for 1000 iterations ")
print(np.mean(paths_1000))
'''
# ------ End Question 2 -----------------------


'''
# --------- Sample result of one map for each search strategy Question 3---------
#Generate cities
cities_locations, cities_distances = generate_map()
#Turn City intro Graph Object
random_map = Graph(cities_distances)
#Generate Random start and goal
start = randint(65,90)
goal = randint(65,90)
#Setup Problem
problem = MapProblem(chr(start),chr(goal),cities_distances,cities_locations)

print("Attempting to solve from " + chr(start) + " to " + chr(goal))

#Print Results for BFS
result_bfs = breadth_first_search(problem)
node, path_back = result_bfs, []
while node:
		path_back.append(node.state)
		node = node.parent
print("Solution from BFS")
print(list(reversed(path_back)))

#Print Results for DFS
result_dfs = depth_first_search(problem)
node, path_back = result_dfs, []
while node:
		path_back.append(node.state)
		node = node.parent
print("Solution from DFS")
print(list(reversed(path_back)))

#Print Results for IDS
result_ids = iterative_deepening_search(problem)
node, path_back = result_ids, []
while node:
		path_back.append(node.state)
		node = node.parent
print("Solution from IDS")
print(list(reversed(path_back)))

#------------- End Question 3 -------------------------------------
'''

#----------------------------------------------
#------------- Question 4 ---------------------
#----------------------------------------------

'''
#-------------Statistic Generation for BFS --------------------
start_time_bfs = time.time()
nodes_generated = []
nodes_visited = []
path_lengths = []
problems_solved = 0
for i in range(100):
	#Generate cities
	cities_locations, cities_distances = generate_map()
	#Turn City intro Graph Object
	random_map = Graph(cities_distances,True)
	#Generate Random start and goal
	start = randint(65,90)
	goal = randint(65,90)
	#Setup Problem
	problem = MapProblem(chr(start),chr(goal),cities_distances,cities_locations)

	print("Attempting to solve from " + chr(start) + " to " + chr(goal))

	if breadth_first_search(problem) is not None:
		solution, explored, nodes_gen = breadth_first_search(problem,stats=True)
	else:
		continue

	node = solution
	solution_length = 0
	while node:
		solution_length+=1
		node = node.parent

	if solution_length != 0:
		problems_solved+=1
		path_lengths.append(solution_length)
	nodes_generated.append(nodes_gen)
	nodes_visited.append(len(explored))
	

print("Average Space Complexity (max nodes generated) %f" %np.max(nodes_generated))
print("Average Time Complexity (nodes visited) %f" %np.mean(nodes_visited))
print("Total BFS Execution Time %s" % (time.time() - start_time_bfs))
print("Average path length %f" %np.mean(path_lengths))
print("Total problems solved %f" %problems_solved)

#----------- End Static Generation for BFS ----------------------------------------
'''
'''
#-------------Statistic Generation for DFS --------------------
start_time_dfs = time.time()
nodes_generated = []
nodes_visited = []
path_lengths = []
problems_solved = 0
for i in range(100):
	#Generate cities
	cities_locations, cities_distances = generate_map()
	#Turn City intro Graph Object
	random_map = Graph(cities_distances,False)
	#Generate Random start and goal
	start = randint(65,90)
	goal = randint(65,90)
	#Setup Problem
	problem = MapProblem(chr(start),chr(goal),cities_distances,cities_locations)

	print("Attempting to solve from " + chr(start) + " to " + chr(goal))

	if depth_first_search(problem) is not None:
		solution, explored, nodes_gen = depth_first_search(problem,stats=True)
	else:
		continue

	node = solution
	solution_length = 0
	while node:
		solution_length+=1
		node = node.parent

	if solution_length != 0:
		problems_solved+=1
		path_lengths.append(solution_length)
	nodes_generated.append(nodes_gen)
	nodes_visited.append(len(explored))
	

print("Average Space Complexity (max nodes generated) %f" %np.max(nodes_generated))
print("Average Time Complexity (nodes visited) %f" %np.mean(nodes_visited))
print("Total DFS Execution Time %s" % (time.time() - start_time_dfs))
print("Average path length %f" %np.mean(path_lengths))
print("Total problems solved %f" %problems_solved)

#----------- End Static Generation for DFS ----------------------------------------

'''
'''
#-------------Statistic Generation for IDS --------------------
start_time_ids = time.time()
nodes_generated = []
nodes_visited = []
path_lengths = []
problems_solved = 0
for i in range(100):
	#Reset IDS stats helper
	ids_visited = 0
	ids_generated = 0

	#Generate cities
	cities_locations, cities_distances = generate_map()
	#Turn City intro Graph Object
	random_map = Graph(cities_distances,True)
	#Generate Random start and goal
	start = randint(65,90)
	goal = randint(65,90)
	#Setup Problem
	problem = MapProblem(chr(start),chr(goal),cities_distances,cities_locations)

	print("Attempting to solve from " + chr(start) + " to " + chr(goal))

	solution = iterative_deepening_search(problem)

	node = solution
	solution_length = 0
	while node:
		solution_length+=1
		node = node.parent

	if solution_length != 0:
		problems_solved+=1
		path_lengths.append(solution_length)
	nodes_generated.append(ids_generated)
	nodes_visited.append(ids_visited)
	

print("Average Space Complexity (max nodes generated) %f" %np.max(nodes_generated))
print("Average Time Complexity (nodes visited) %f" %np.mean(nodes_visited))
print("Total IDS Execution Time %s" % (time.time() - start_time_ids))
print("Average path length %f" %np.mean(path_lengths))
print("Total problems solved %f" %problems_solved)

#----------- End Static Generation for IDS ----------------------------------------
'''
#----------------------------------------------
#------------- END Question 4 -----------------
#----------------------------------------------


#----------------------------------------------
#------------- Question 5 ---------------------
#----------------------------------------------
'''
#-------------Statistic Generation for GBFS--------------------
start_time_gbfs = time.time()
nodes_generated = []
nodes_visited = []
path_lengths = []
problems_solved = 0
for i in range(100):
	#Generate cities
	cities_locations, cities_distances = generate_map()
	#Turn City intro Graph Object
	random_map = Graph(cities_distances,False)
	#Generate Random start and goal
	start = randint(65,90)
	goal = randint(65,90)
	#Setup Problem
	problem = MapProblem(chr(start),chr(goal),cities_distances,cities_locations,'m')

	print("Attempting to solve from " + chr(start) + " to " + chr(goal))

	if greedy_best_first_search(problem) is not None:
		solution, explored, nodes_gen = greedy_best_first_search(problem,stats=True)
	else:
		continue

	node = solution
	solution_length = 0
	while node:
		solution_length+=1
		node = node.parent

	if solution_length != 0:
		problems_solved+=1
		path_lengths.append(solution_length)
	nodes_generated.append(nodes_gen)
	nodes_visited.append(len(explored))
	
print("Average Space Complexity (max nodes generated) %f" %np.max(nodes_generated))
print("Average Time Complexity (nodes visited) %f" %np.mean(nodes_visited))
print("Total GBFS Execution Time %s" % (time.time() - start_time_gbfs))
print("Average path length %f" %np.mean(path_lengths))
print("Total problems solved %f" %problems_solved)

#----------- End Static Generation for GBFS ----------------------------------------
'''
'''
#-------------Statistic Generation for A*--------------------
start_time_a_star = time.time()
nodes_generated = []
nodes_visited = []
path_lengths = []
problems_solved = 0
for i in range(100):
	#Generate cities
	cities_locations, cities_distances = generate_map()
	#Turn City intro Graph Object
	random_map = Graph(cities_distances,True)
	#Generate Random start and goal
	start = randint(65,90)
	goal = randint(65,90)
	#Setup Problem
	problem = MapProblem(chr(start),chr(goal),cities_distances,cities_locations,'m')

	print("Attempting to solve from " + chr(start) + " to " + chr(goal))

	if a_star_search(problem) is not None:
		solution, explored, nodes_gen = a_star_search(problem,stats=True)
	else:
		continue

	node = solution
	solution_length = 0
	while node:
		solution_length+=1
		node = node.parent

	if solution_length != 0:
		problems_solved+=1
		path_lengths.append(solution_length)
	nodes_generated.append(nodes_gen)
	nodes_visited.append(len(explored))
	
print("Average Space Complexity (max nodes generated) %f" %np.max(nodes_generated))
print("Average Time Complexity (nodes visited) %f" %np.mean(nodes_visited))
print("Total A* Execution Time %s" % (time.time() - start_time_a_star))
print("Average path length %f" %np.mean(path_lengths))
print("Total problems solved %f" %problems_solved)

#----------- End Static Generation for A* ----------------------------------------
'''

#----------------------------------------------
#------------- END Question 5 -----------------
#----------------------------------------------

'''
#Uniformed Search Strategies Experimentation
for i in range(0):
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

	result_a = a_star_search(problem)

	node, path_back = result_a, []
	while node:
		path_back.append(node.state)
		node = node.parent
	print(list(reversed(path_back)))

'''