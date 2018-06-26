from kanren import run, Relation, facts, var, conde
parent = Relation()
facts (parent, ( "Darth Vader","Luke Skywalker"),
				("Darth Vader", "Leia Organa"),
				("Leia Organa","Kylo Ren"),
				("Han Solo", "Kylo Ren"))

x=var()

print(run(1,x,parent(x,"Luke Skywalker")))

print(run(2,x,parent("Darth Vader",x)))

def grandparent(x,z):
	y = var()
	return conde((parent(x,y),parent(y,z)))

print(run(1,x,grandparent(x,'Kylo Ren')))