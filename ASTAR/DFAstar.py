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

#Midpoints of graph in order to configure position
#Given negative or positive x and y
MidX = 0
MidY = 0

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
    global ENV
    #P = []
    #P.insert(0,PathSeq[-1])
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
		    ENV[PathSeq[k][0]][PathSeq[k][1]] = 4
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
	    #elif(i[3]==PathSeq[k][0] and i[4]==PathSeq[k][1]):
		#P.insert(0,PathSeq[k])
	    #print("")
	#print("")
	i = PathSeq[k]
	k-=1

    #P.insert(0,PathSeq[0])
    #PathSeq = P
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
    #return 1.0 
    ################################### STANDARD A* COST
    return 0.01

def grid(x,y):
    if(x<0 or x>len(ENV) or y<0 or y>len(ENV)):
	print ("LINE OF SIGHT::Out of Bounds")
	#sys.exit(-2)
	return False
    return ENV[x][y]==0

#[y,x,f,py,px,dfp]
def LineOfSight(s1,s2):
    if(s1 is None or s2 is None):
	return False
    x_0 = s1[1]
    y_0 = s1[0]
    x_1 = s2[1]
    y_1 = s2[0]
    F = 0
    d_y = y_1-y_0
    d_x = x_1-x_0
    s_y = 0
    s_x = 0
    
    if d_y<0:
        d_y=d_y*-1
	s_y = -1
    else:
	s_y = 1
    if d_x<0:
	d_x=d_x*-1
	s_x = -1
    else:
	s_x=1
    
    if d_x>=d_y:
	while x_0!=x_1:
	    F=F+d_y
	    if F>=d_x:
		if grid(x_0+((s_x-1)/2),y_0+((s_y-1)/2)):
		    return False
		y_0=y_0+s_y
		F = F - d_x

	    if F!=0 and grid(x_0 + ((s_x-1)/2),y_0+((s_y-1)/2)):
	        return False

	    if d_y==0 and grid(x_0 + ((s_x-1)/2),y_0) and grid(x_0 + ((s_x-1)/2),y_0-1):
		return False
	    x_0=x_0+s_x
    else:
	while y_0!=y_1:
	    F=F+d_x
	    if F>=d_y:
		if grid(x_0+((s_x-1)/2),y_0+((s_y-1)/2)):
		    return False
		x_0=x_0 + s_x
		F = F - d_y
	    if F!=0 and grid(x_0 + ((s_x-1)/2),y_0+((s_y-1)/2)):
		return False
	    if d_x==0 and grid(x_0,y_0 + ((s_y-1)/2)) and grid(x_0-1,y_0+((s_y-1)/2)):
		return False
	    y_0 = y_0 + s_y
    return True
def Parent(S):
    i = None
    p = []
    p.append(S[3])
    p.append(S[4])
    #k = 0
    for i in PathSeq:
	print("IF:",p,"==",i)
	if(p[0] == i[0] and p[1] ==i[1]):
	    print("Found Parent of:",S)
	    ##sys.exit(-1)
	    return i
    print("FOUND NO PARENT")
    return None
	#k+=1	
#Chooses optimal path
#s1, s2 are State Classes
def UpdateVertex(s1,s2):
    global F   
 
    First = s1
    Second = s2
   
    print("FIRST:",First,"SECOND:",Second, "GOAL:",Goal)

    C = 0.0

    C += Cost(First,Second) #+ s2[2]

    #H = Heuristic(s2)

    #s2[2]
    
    #############################################################################	
    #Check if found a shorter adjacent path
    print ("VALUE:",First[5]+C, "<", s2[5], "??")
    #############################################################################

    #print("LINE OF SIGHT:",LineOfSight(s1,s2))
    P = Parent(s1)	

    C2 = C+Cost(P,Second)

    if LineOfSight(P,s2):
	#Path 2
	if P[5] + C2 < Second[5]:
	    #Found a better path for LOS, new parent
	    Second[5] = round(P[5] + C2,2)
	    Second[3] = First[3]
	    Second[4] = First[4]

	    if(F.Exists(Second)):
		F.Remove(Second[0],Second[1])

	    Second[2] = Heuristic(Second)+Second[5]

            print("s2 F VALUE CASE 1:",Second[2])

	    F.Insert(Second)
    else:
	#Path 1

        if(First[5] + C < s2[5]):

	    #Found a better path, new parent	
	    s2[5] = round(First[5] + C,2)
	    s2[3] = First[0]
	    s2[4] = First[1]
            ################################

	    #If the fringe already contains s2, remove it, BECAUSE FOUND A SHORTER ADJ PATH	
	    if(F.Exists(s2)):
	        F.Remove(s2[0],s2[1])
        
	    s2[2] = Heuristic(s2) + s2[5]
	
            print("s2 F VALUE CASE 2:",s2[2])

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
    return round((math.ceil(math.sqrt(2)*min(abs(End[0]-Start[0]),abs(End[1]-Start[1])) + max(abs(End[0]-Start[0]),abs(End[1]-Start[1])) - min(abs(End[0]-Start[0]),abs(End[1]-Start[1])))/100),2)
    

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
	GoTo.append([TempY,TempX,(S[5]+0.01)+Heuristic([TempY,TempX]),StartY,StartX,S[5]+0.01])

    #DOWN 
    TempX = StartX
    TempY = StartY+1
    #print("Temp X:",TempX," TempY: ",TempY)
    if(ClearToGo(TempY,TempX)and (P[0]!=TempY or P[1]!=TempX)):
        GoTo.append([TempY,TempX,S[5]+0.01+Heuristic([TempY,TempX]),StartY,StartX,S[5]+0.01])

    #LEFT 
    TempX = StartX-1
    TempY = StartY
    #print("Temp X:",TempX," TempY: ",TempY)    
    if(ClearToGo(TempY,TempX)and (P[0]!=TempY or P[1]!=TempX)):
        GoTo.append([TempY,TempX,S[5]+0.01+Heuristic([TempY,TempX]),StartY,StartX,S[5]+0.01])

    #RIGHT 
    TempX = StartX+1
    TempY = StartY
    #print("Temp X:",TempX," TempY: ",TempY)
    if(ClearToGo(TempY,TempX)and (P[0]!=TempY or P[1]!=TempX)):
        GoTo.append([TempY,TempX,S[5]+0.01+Heuristic([TempY,TempX]),StartY,StartX,S[5]+0.01])

    #UpRIGHT
    TempX = StartX+1
    TempY = StartY-1
    #print("Temp X:",TempX," TempY: ",TempY)    
    if(ClearToGo(TempY,TempX)and (P[0]!=TempY or P[1]!=TempX)):
        GoTo.append([TempY,TempX,S[5]+0.01+Heuristic([TempY,TempX]),StartY,StartX,S[5]+0.01])

    #UPLEFT
    TempX = StartX-1
    TempY = StartY-1
    #print("Temp X:",TempX," TempY: ",TempY)
    if(ClearToGo(TempY,TempX)and (P[0]!=TempY or P[1]!=TempX)):
        GoTo.append([TempY,TempX,S[5]+0.01+Heuristic([TempY,TempX]),StartY,StartX,S[5]+0.01])

    #DownLeft 
    TempX = StartX-1
    TempY = StartY+1
    #print("Temp X:",TempX," TempY: ",TempY)
    if(ClearToGo(TempY,TempX)and (P[0]!=TempY or P[1]!=TempX)):
        GoTo.append([TempY,TempX,S[5]+0.01+Heuristic([TempY,TempX]),StartY,StartX,S[5]+0.01])

    #DownRight
    TempX = StartX+1
    TempY = StartY+1
    #print("Temp X:",TempX," TempY: ",TempY)
    if(ClearToGo(TempY,TempX) and (P[0]!=TempY or P[1]!=TempX)):
        GoTo.append([TempY,TempX,S[5]+0.01+Heuristic([TempY,TempX]),StartY,StartX,S[5]+0.01])

    if(len(GoTo)==0):
	print("")
	print("Nowhere to go from:",StartY,StartX)

    print("GOTO CLEARANCE:",GoTo)
   
    #Return list of successors to S
    return GoTo
def MaxLen():
    global ENV
    global MidX
    global MidY

    i = None
    j = ''
    Ccount = 0
    y = -sys.maxint
    z = -sys.maxint
    for i in ENV:
	Ccount = 0
	print("If:",len(i)," >",y)
	if(len(i)>y):
	    MidX = (len(i)/2.0) 
	    y = len(i)
	for j in i:
	    Ccount+=1
	    #print("If:",len(j)," >",y)
	    #if(len(j)>y):
	        #y = len(j)
	if(Ccount>z):
	    MidY = (Ccount/2.0)
	    z=Ccount
    return y
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
    #print (x)
    PrintENV(x)

###############################################################ASSUME GRID IS NXN#### AND PREFERRABLY EVEN###################################################################  
    L = MaxLen()
    print("MAX LENGTH:",L)
    #Midpoint used to convert neg to pos coordinate numbers for env
    #MidX = math.floor(L/2)
    #MidY = math.ceil(len(x[len(x)-1])/2)
    #MidY = math.floor(L/2)
###############################################################################################################################################################################################

    print("Midpoints: [%d,%d]"%(MidX,MidY))

    #First Entry for goal is x, second is y
    GY = round(float(sys.argv[4]),2)
    GY*=100
    GY = math.ceil(GY)
    GY = int(MidY+GY)
    #if GY<=0 OR GY >0, set position should hold
    GX = round(float(sys.argv[3]),2)
    GX*=100
    GX = math.ceil(GX)
    GX = int(MidX+GX)
    #If GX<=0 OR GX>0, set position should hold
    
    Goal = [GY,GX,0,GY,GX,sys.maxint]

    print( "Goal: [%d,%d]"%(GY,GX) )

    if(Goal[0]<0 or Goal[0]>len(ENV)-1 or Goal[1]<0 or Goal[1]>len(ENV[0])-1):
	print("Goal is Out of bounds")
	return
    
    ENV[Goal[0]][Goal[1]] = 1

    #First Entry for start is x, second is y
    SY = round(float(sys.argv[2]),2)
    SY*=100
    SY = math.ceil(SY)
    SY = int(MidY+SY)
    #If SY<=0 OR SY>0, set position should hold
    SX = round(float(sys.argv[1]),2)
    SX*=100
    SX = math.ceil(SX)
    SX = int(MidX+SX)
    #If SX <=0 OR SX >0, set position should hold   

    S = [SY,SX,0,SY,SX,0]

    #print("sTART:",S);

    if(S[0]<0 or S[0]>len(ENV)-1 or S[1]<0 or S[1]>len(ENV[0])-1):
        print("START is Out of bounds")
        return

    Ss = [SY,SX,Heuristic(S),SY,SX,0]

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
	    #PrintE()
	    print ("FOUND GOAL!")
	    print ("Uncompressed::",PathSeq[:])
	    #print("")
	    ############################################## This is equivalent to parent parent(s) function...
	    Compress()
	    print ("Compressed::",PathSeq[:])
	    PrintE()
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
		    #PrintE()
		
		if(len(O)<3 or len(S)<3):
		    print("ERROR, LENGTH NOT CORRECT")
		    print("S:",S,"O:",O)
		    sys.exit(-1)
				    	    
		(UpdateVertex(S,O))    
	    #print("FRINGE:",F.List)	     
            #t+=1
	    #if t==1000:
	        #return
	#PrintE()
    print ("NO GOAL FOUND!!!!")

if __name__=="__main__":
    main()
