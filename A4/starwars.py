from kanren import run, Relation, facts, var, conde
parent = Relation()
facts (parent, ( "Darth Vader","Luke Skywalker"),
				("Darth Vader", "Leia Organa"),
				("Leia Organa","Kylo Ren"),
				("Han Solo", "Kylo Ren"))

x=var()

#Query ONE parent of Luke Skywalker
print("The parent of Luke Skywalker is:")
print(run(1,x,parent(x,"Luke Skywalker")))

#Query TWO children of Darth Vader
#If we do 1, only the last one is returned
print("The children of Darth Vader are:")
print(run(2,x,parent("Darth Vader",x)))

#Help, function to return
#grandparet of
def grandparent(x,z):
	y = var()
	return conde((parent(x,y),parent(y,z)))

print("The grandparent of Kylo Ren is:")
print(run(1,x,grandparent(x,'Kylo Ren')))



#--------------- 'Standard Python ------------------------

print("\n \n \n Switching to Pure Python \n \n \n")

from collections import defaultdict

#Create a dictionary of lists for parent - children relation
#Each key is the parent, the list is the children
family_parents = defaultdict(list)

#Add children of Darth Vader
family_parents["Darth Vader"].append("Luke Skywalker")

#Add Children of Darth Vader
family_parents["Darth Vader"].append("Leia Organa")

#Add Children of Leia
family_parents["Leia Organa"].append("Kylo Ren")

#Add Children of Han
family_parents["Han Solo"].append("Kylo Ren")

def get_parents(name):
	parents = []
	for k in family_parents:
		if name in family_parents[k]:
			parents.append(k)
	return parents

def get_children(name):
	return family_parents[name]

def get_grandparent(name):
	parents = get_parents(name)
	grandparents = []
	for i in parents:
		g = get_parents(i)
		for j in g:
			if j not in grandparents:
				grandparents.append(j)
	return grandparents

print("The parent of Luke Skywalker is:")
luke_parent = get_parents("Luke Skywalker")
print(luke_parent)
print("The children of Darth Vader are:")
darth_children = get_children("Darth Vader")
print(darth_children)
print("The grandparent of Kylo Ren is:")
kylo_grandparent = get_grandparent("Kylo Ren")
print(kylo_grandparent)
	
