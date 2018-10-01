from EnvGen import EnvGen
from MapMake import mapMake
from VisibilityGraph import computeVisibilityGraph, addStartGoal, deleteStartGoal

import sys
class StartEGen():
    
    def __init__(self,M,SG):
	self.Map = M
	self.Start_Goals = SG

def main(S):
    if(len(sys.argv[:])<2 and S==sys.argv[:]):
        print("MUST ENTER MAP PATH IN ARG 1")
	sys.exit(-1)
    if(S!=sys.argv[:]):
	print "Another program started this script"
    print("Start")
    E = EnvGen()
    E2 = []
    if(S==sys.argv[:]):
        E2 = E.CreateENV(sys.argv[1])
    else:
	E2 = E.CreateENV(S)

    i = None
    k = 0
    E3 = []

    for i in E2:
	if(i[0]=='-Start+Goal Pairs-'):
	    j = None
	    for j in E2[k:]:
	        if(j[0]!='NEXT LINE'):
		    E3.append(j)
	    E3.pop(0)
	    break

    	k+=1
    ################################START GOAL PAIR
    #print "NEW E2:",E3
    ###############################################
    M = mapMake(E2)
    graph = computeVisibilityGraph(E2, M)
    print "Graph V1: \n", graph

    start = (float(E3[0][0]), float(E3[0][1]))
    goal = (float(E3[1][0]), float(E3[1][1]))
    addStartGoal(graph, M, start, goal)
    print "Graph V2: \n", start, graph[start]
    deleteStartGoal(graph, start, goal)
    print "Graph V3: \n", graph
    ##########MAP
    #print("MAP:",M,"Size:",len(M))
    SGEN = StartEGen(M,E3)

    #print("SGEN MAP:",SGEN.Map," SGEN STARt/GOALS:", SGEN.Start_Goals)
    return SGEN
if __name__=="__main__":
    main(sys.argv[:])
