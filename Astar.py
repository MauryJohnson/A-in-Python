#import Fringe
#import ClosedList
#from ClosedList import ClosedList
from __future__ import print_function
import math
from Fringe import Fringe
#from State import State

from argparse import ArgumentParser

import sys

from numpy import loadtxt

#Visited/Closed List
ClosedList =  []

#Fringe List
F = Fringe()

#Rows, Columns
ENV = []

#Goal = []

#Goal =[5,5,0,5,5]
Goal = []

PathSeq = []

#Remove Redundancies to have one path
#Each node kept track of parent, so when reach goal, follow correct parents until reach start
#SINCE each node only has one parent after it's visited, solution will be one path
#Pop each redundant node
def Compress():
    global PathSeq
    i = []
    k = len(PathSeq)-1
    while k>=0:
	if(len(i)>4):
	    #If suboptimal node
	    sv = k
	    ct = 0
	    if(i[3]!=PathSeq[k][0] or i[4]!=PathSeq[k][1]):
	        while(i[3]!=PathSeq[k][0] or i[4]!=PathSeq[k][1]): #and i[2] > PathSeq[k][2]):
		    print("POP NODES not Ancestors of GOAL PATH",PathSeq[k])
		    PathSeq.pop(k)
		    k-=1
		    if k<0:
		        break
		    ct+=1
	        #IF duplicate node
	        k = sv-ct
		print("")
	    elif(i==PathSeq[k]):
	        PathSeq.pop(k)
	    #print("")
	#print("")
	i = PathSeq[k]
	k-=1

###########################################
#INSTEAD OF STATE, USE [row,col,f(n),ParRow,ParCol]
#Takes care of state.Parent
###########################################

def PrintE():
    global ENV
    
    i  = ' '
    #
    for i in ENV:
	print(i)
	print("")

def PrintENV(x):
    i = ''
    p1 = 0
    for i in x:
        k = '0'
	success = False
	#p2=0
	Succ  = []
	for k in i:
	    if(k==''):
	 	break
	    if(k!=''):
	        try:
		     success=True
		     #print (int(k))
		     print(int(k),end=' ')
		except:
		     success = False
		if(success):
		    Succ.append(int(k))
	ENV.append(Succ)
	p1+=1
	print ("")


def Cost(s1,s2): #... IS 1 for traditional A*, but is dependant on the diagonal dist for free-direction A*
    print ("Cost Func from Coordinates of s1 to Coordinates of s2")
    print (s1)
    print (s2)
    print ("+1")
    ################################### STANDARD A* COST
    return 1 
    ################################### STANDARD A* COST


#Chooses optimal path
#s1, s2 are State Classes
def UpdateVertex(s1,s2):
    global F   
 
    First = s1
    Second = s2
   
    print("FIRST:",First,"SECOND:",Second, "GOAL:",Goal)

    C = 0

    C = Cost(First,Second) #+ s2[2]

    #H = Heuristic(s2)

    #s2[2]
    
    #############################################################################	
    #Check if found a shorter adjacent path
    print ("VALUE:",First[5]+C, "<", s2[5], "??")
    #############################################################################

    if(First[5] + C < s2[5]):

	#Found a better path, new parent	
	s2[5] = First[5] + C
	s2[3] = First[0]
	s2[4] = First[1]
        ################################

	#If the fringe already contains s2, remove it, BECAUSE FOUND A SHORTER ADJ PATH	
	if(F.Exists(s2)):
	    F.Remove(s2[0],s2[1])
        
	s2[2] = Heuristic(s2) + s2[5]
	
        print("s2 F VALUE:",s2[2])

        F.Insert(s2)
    
    #if(len(F.List)>50000):
            #sys.exit(0)
	#Insert new s2 along with new G in fring
    
    return s2

#Returns Cumputed Heuristic given s1,s2 states.
def Heuristic(s1):
    Start = s1
    End = Goal
    
    print()
    print()
    print("END",End,"START",Start)
    print()
    print()

    #Manhattah Heuristic
    #return abs(End[0]-Start[0]) + abs(End[1]-Start[1])
    
    #Euclidean Heuristic
    #return int(math.ceil(math.sqrt((End[0]-Start[0])*(End[0]-Start[0]) + (End[1]-Start[1])*(End[1]-Start[1]) )))
    
    #Trace A* Heuristic
    return int(math.ceil(math.sqrt(2)*min(abs(End[0]-Start[0]),abs(End[1]-Start[1])) + max(abs(End[0]-Start[0]),abs(End[1]-Start[1])) - min(abs(End[0]-Start[0]),abs(End[1]-Start[1]))))
    

#Checks if ENV representation is correct
def ClearToGo(Y,X):
    print("Clear To Go check:",Y,X,"Length ENV:",len(ENV),len(ENV[0]))
    if(X<0 or Y<0 or X>len(ENV[0])-1 or Y>len(ENV)-1):
 	print ("Out of Bounds, hit a boundary")
	return False
    if(ENV[Y][X]==1):
	print("")
	print("Clear to Go To:",Y,X)
	print("")
	return True
    return False

#Returns List of positions to go to

#[ROW,COL,F(N),PRow,PCol,G(N)]

def NonCollisions(S):
    print ("Non Collisions for ENV")
    #Up(x,y-1),Down(x,y+1),Left)x-1,y), Right(x+1,y), UpRight (x+1,y+1),Up Left(x-1,y+1), DownLeft(x-1,y-1), DownRight (x+1,y-1)
    print ("SSSSSSSS:",S)
    P = []
    P.append(S[3])
    P.append(S[4])
    #P[0] = S[3]
    #P[1] = S[4] 
    print("START:",S,"Parent:",P)

    #Rows
    StartY = S[0]
    #Cols
    StartX = S[1]

    GoTo = []    
    
    #UP 
    TempX = StartX
    TempY = StartY-1 
    #print("Temp X:",TempX," TempY: ",TempY)
    if(ClearToGo(TempY,TempX) and (P[0]!=TempY or P[1]!=TempX)):
	GoTo.append([TempY,TempX,(S[5]+1)+Heuristic([TempY,TempX]),StartY,StartX,S[5]+1])

    #DOWN 
    TempX = StartX
    TempY = StartY+1

    #print("Temp X:",TempX," TempY: ",TempY)
    if(ClearToGo(TempY,TempX)and (P[0]!=TempY or P[1]!=TempX)):
        GoTo.append([TempY,TempX,S[5]+1+Heuristic([TempY,TempX]),StartY,StartX,S[5]+1])

    #LEFT 
    TempX = StartX-1
    TempY = StartY
    #print("Temp X:",TempX," TempY: ",TempY)    
    if(ClearToGo(TempY,TempX)and (P[0]!=TempY or P[1]!=TempX)):
        GoTo.append([TempY,TempX,S[5]+1+Heuristic([TempY,TempX]),StartY,StartX,S[5]+1])

    #RIGHT 
    TempX = StartX+1
    TempY = StartY
    #print("Temp X:",TempX," TempY: ",TempY)
    if(ClearToGo(TempY,TempX)and (P[0]!=TempY or P[1]!=TempX)):
        GoTo.append([TempY,TempX,S[5]+1+Heuristic([TempY,TempX]),StartY,StartX,S[5]+1])

    #UpRIGHT
    TempX = StartX+1
    TempY = StartY-1
    #print("Temp X:",TempX," TempY: ",TempY)    
    if(ClearToGo(TempY,TempX)and (P[0]!=TempY or P[1]!=TempX)):
        GoTo.append([TempY,TempX,S[5]+1+Heuristic([TempY,TempX]),StartY,StartX,S[5]+1])

    #UPLEFT
    TempX = StartX-1
    TempY = StartY-1
    #print("Temp X:",TempX," TempY: ",TempY)
    if(ClearToGo(TempY,TempX)and (P[0]!=TempY or P[1]!=TempX)):
        GoTo.append([TempY,TempX,S[5]+1+Heuristic([TempY,TempX]),StartY,StartX,S[5]+1])

    #DownLeft 
    TempX = StartX-1
    TempY = StartY+1
    #print("Temp X:",TempX," TempY: ",TempY)
    if(ClearToGo(TempY,TempX)and (P[0]!=TempY or P[1]!=TempX)):
        GoTo.append([TempY,TempX,S[5]+1+Heuristic([TempY,TempX]),StartY,StartX,S[5]+1])

    #DownRight
    TempX = StartX+1
    TempY = StartY+1
    #print("Temp X:",TempX," TempY: ",TempY)
    if(ClearToGo(TempY,TempX)and (P[0]!=TempY or P[1]!=TempX)):
        GoTo.append([TempY,TempX,S[5]+1+Heuristic([TempY,TempX]),StartY,StartX,S[5]+1])

    if(len(GoTo)==0):
	print("")
	print("Nowhere to go from:",StartY,StartX)

    print("GOTO CLEARANCE:",GoTo)
   
    #Return list of successors to S
    return GoTo
def main():
    global Goal
    global ENV
    global ClosedList
    global PathSeq
    global F

    if(len(sys.argv[:])<5):
        print("MUST ENTER START [row,col] ARGuMENT AND GOAL [row,col] ARGUMENT!")
	sys.exit(-1)

    #parser = ArgumentParser()
    #parser.add_argument("-s","--Startr")
    #parser.add_argument("-t","--Startc")
    #parser.add_argument("-u","--Goalr")
    #parser.add_argument("-v","--Goalc")

    #args = parser.parse_args()

    #if( args.Startr is None or args.Startc is None or args.Goalr is None or args.Goalc is None):
	#print("MUST ENTER START [row,col] ARGuMENT AND GOAL [row,col] ARGUMENT!")
	#sys.exit(-1)

    #print("hello World")    
    #F = Fringe()
    #F.Insert(5,2,20)
    #F.Insert(6,7,-2)
    #F.Insert(21,23,22)
    #F.Print()    
    #P = F.Pop()
    #F.Print()
    #F.Remove(21,23)
    #F.Print()
    #      TEST
    #ASTAR

    f = open('maze','r')
    x = f.read().splitlines()
    f.close()
    print ("Array")
    print (x)
    PrintENV(x)
   
    Goal = [int(sys.argv[3]),int(sys.argv[4]),0,int(sys.argv[3]),int(sys.argv[4]),sys.maxint]

    if(Goal[0]<0 or Goal[0]>len(ENV)-1 or Goal[1]<0 or Goal[1]>len(ENV[0])-1):
	print("Goal is Out of bounds")
	return
    
    ENV[Goal[0]][Goal[1]] = 1

    S = [int(sys.argv[1]),int(sys.argv[2]),0,int(sys.argv[1]),int(sys.argv[2]),0]

    #print("sTART:",S);

    if(S[0]<0 or S[0]>len(ENV)-1 or S[1]<0 or S[1]>len(ENV[0])-1):
        print("START is Out of bounds")
        return

    Ss = [int(sys.argv[1]),int(sys.argv[2]),Heuristic(S),int(sys.argv[1]),int(sys.argv[2]),0]

    S = Ss

    #Be sure that you insert triplets into the fringe
    
    #Initially Cost is 0 FOR CLASSICAL A*
    F.Insert(Ss)
    
    print("FRINGE:",F.List)
   
    if(ENV == []):
	print ("No ENV to perform A*")
	return 

    PathSeq.append(Ss)

    SList = []

    #Expand then evaluate
    while(F.List!=[]):

        S = F.Pop()      

	#if(S[3]==PathSeq[-1][0] and S[4] == PathSeq[-1][1]):  
	PathSeq.append(S)
        ENV[S[0]][S[1]] = 2
	#else:
	    #print("FAILED WITH:",S,"AND PSEQ:",PathSeq)
	    #ENV[S[0]][S[1]] = -2
	    #sys.exit(0)
	    #continue

	if S[0]==Goal[0] and S[1]==Goal[1]:
	    PrintE()
	    print ("FOUND GOAL!")
	    print ("Uncompressed::",PathSeq[:])
	    print("")
	    ############################################## This is equivalent to parent parent(s) function...
	    Compress()
	    print ("Compressed::",PathSeq[:])
	    return PathSeq[:]
	
	ClosedList.append(S)

        #List of tuple successors
	
	L = NonCollisions(S)

	print("ALL NON COLLISIONS:",L)
        u = []
	O = []
	#U = State()
	print("CLOSED LISTS",ClosedList)	
	#Check if already visited and not in fringe
	#t = 0
	for u in L:
	    if u not in ClosedList:
		
		print(u," is not visited YET")
		
		if not F.Exists(u):
		    print(u," is not in fringe YET")
		    
		    O = u
		    O[3] = -1
		    O[4] = -1
   	 	    O[5] = sys.maxint
		    
   	 	    ENV[u[0]][u[1]] = 3
		    PrintE()
		
		if(len(O)<3 or len(S)<3):
		    print("ERROR, LENGTH NOT CORRECT")
		    print("S:",S,"O:",O)
		    sys.exit(-1)
				    	    
		(UpdateVertex(S,O))    
	    print("FRINGE:",F.List)	     
            #t+=1
	    #if t==1000:
	        #return
	PrintE()
    print ("NO GOAL FOUND!!!!")

if __name__=="__main__":
    main()
