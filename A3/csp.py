from constraint import *

problem = Problem()
problem.addVariable("F",[0,1,2,3,4,5,6,7,8,9])
problem.addVariable("T",[0,1,2,3,4,5,6,7,8,9])
problem.addVariable("U",[0,1,2,3,4,5,6,7,8,9])
problem.addVariable("W",[0,1,2,3,4,5,6,7,8,9])
problem.addVariable("R",[0,1,2,3,4,5,6,7,8,9])
problem.addVariable("O",[0,1,2,3,4,5,6,7,8,9])
problem.addVariable("C10",[0,1,2,3,4,5,6,7,8,9])
problem.addVariable("C100",[0,1,2,3,4,5,6,7,8,9])
problem.addVariable("C1000",[1,2,3,4,5,6,7,8,9])

problem.addConstraint(lambda F,T,U,W,R,O: F != T and F != U and F != W and F!= R and F!=O,("F","T","U","W","R","O"))
problem.addConstraint(lambda F,T,U,W,R,O: T != F and T != U and T != W and T!= R and T!=O,("F","T","U","W","R","O"))
problem.addConstraint(lambda F,T,U,W,R,O: U != F and U != T and U != W and U!= R and U!=O,("F","T","U","W","R","O"))
problem.addConstraint(lambda F,T,U,W,R,O: W != F and W != T and W != U and W!= R and W!=O,("F","T","U","W","R","O"))
problem.addConstraint(lambda F,T,U,W,R,O: R != F and R != T and R != U and R!= W and R!=O,("F","T","U","W","R","O"))
problem.addConstraint(lambda F,T,U,W,R,O: O != F and O != T and O != U and O!= W and O!=R,("F","T","U","W","R","O"))

#problem.addConstraint(AllDifferentConstraint())
problem.addConstraint(lambda O,R,C10: O + O == R + (10 * C10), ("O","R","C10"))
problem.addConstraint(lambda W,U,C100: W + W == U + (10 * C100), ("W","U","C100"))
problem.addConstraint(lambda T,O,C1000: T + T == O + (10 * C1000), ("T","O","C1000"))
problem.addConstraint(lambda F,C1000: C1000 == F, ("F","C1000"))
#problem.addConstraint(lambda F,T,U,W,R,O: T + T + W + W + O + O == F + O + U + R, ("F","T","U","W","R","O"))


print(problem.getSolutions())

