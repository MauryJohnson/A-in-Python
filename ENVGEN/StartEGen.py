from EnvGen import EnvGen
from MapMake import mapMake
import math
import sys

#ENV CAN EVEN JUST BE LIST OF ALL BLOCKS AND THEIR AREAS
#Also Get 
#ENV = []
#EnvTable = []

class StartEGen():   
    def __init__(self,VL,SG,ENVS):
	self.EnvTable = []
 	self.ENV = []
	self.Y = -1
	self.X = -1
 	self.Map = []
	#Should only keep track of the next start goal pair to use
	self.Start_Goals = SG
	self.Vertex_List = VL
	#Generate entire 2D ENV WITH BLOCKS
 	self.GenEnv(ENVS,VL)
  	#Initialize start, goal, block vertices
	#USE IN TESTRUN FOR EVERY SG PAIR
########self.InitializeTable(VL)
	#USE IN TESTRUN FOR EVERY SG PAIR
        #Build entire table for A,DFA*
#########self.BuildTable(SG[0],SG[1])
	

    #EnvTable[0] - > Vertex 1 -> Neighbors of V1
    #EnvTable[0][0] -> Vertex 1
    #EnvTable[0][0][0] -> Vertex 1[0]
    #EnvTable[0][0][1] -> Vertes 1[1]
    
    #Generate entire 2D ENV WITH BLOCKS

    def Distance(self,Pairs):
        print "Compute distance"
	X = math.pow(float(Pairs[1][0])-float(Pairs[0][0]),2)

	Y = math.pow(float(Pairs[1][1])-float(Pairs[0][1]),2)

 	return round(math.sqrt(X+Y),2)

    
    def GenEnv(self,ENVS,VtexList):
	if(ENVS==[] or VtexList==[]):
	    print "No 2D ENV to GEN"
	    sys.exit(-1)
	print "Gen ENV AREA"

	#MaxLen = -sys.maxint
	prev = None
	Pairs = []
 	#Oriented points clockwise, get two side lengths to get area Y*X
	i = 0
	#ADJACENT PAIRS
	#Even,ODD,EVEN,ODD
	MaxEnvYX = [-sys.maxint,-sys.maxint]
	print ""
	while i<len(ENVS):
	    if(len(Pairs)>=2):
		print "ENV PAirs",Pairs
		if Pairs[0][0]!='NEXT LINE':
		    print self.Distance(Pairs)
		i-=1
		Pairs = []
		continue
	    else:
		Pairs.append(ENVS[i])
	        i+=1
		continue
	print "ENV PAirs",Pairs
	if Pairs[0][0]!='NEXT LINE':
	    print "Distance:", self.Distance(Pairs)

	Pairs = []
	i = 0
	NLine  =False
	MaxVtexYX = [-sys.maxint,-sys.maxint]
	while i<len(VtexList):
	    if(len(Pairs)>=2):
		if(Pairs[1][0]=='NEXT LINE'):
		    Pairs[0]=['NEXT LINE']
		print "BLOCK PAirs",Pairs
		if Pairs[0][0]!='NEXT LINE':
		    print "Distance:", self.Distance(Pairs)
		i-=1
		Pairs = []
		NLine = False
		continue
	    else:
		if(VtexList[i][0]=='NEXT LINE' or NLine):
		    Pairs.append(['NEXT LINE'])
		    #Pairs.append(['NEXT LINE'])	
		    NLine = True
		    i+=1
		    continue	
		else:		
		    Pairs.append(VtexList[i])
	        i+=1
		continue
	print "BLOCK PAirs",Pairs
	if Pairs[0][0]!='NEXT LINE':
	    print "Distance:",self.Distance(Pairs)

	sys.exit(0)
    #Add all Block Vertices and start, goal vertices to table
    def InitializeTable(self,VtexList,SG):
	if(VtexList==[]):
	    print "No Vertices given"
	    sys.exit(-1)	
	self.EnvTable = []
	L = [SG[0],['TEST S']]
	self.EnvTable.append(L)
	L = [SG[1],['TEST G']]
	self.EnvTable.append(L)
	for i in VtexList:
	    L = [i,['TEST NEIGHBORS']]
	    self.EnvTable.append(L)
	#EnvTable[0].append(['SECOND NEIGH'])
  	print self.EnvTable

    #Build entire table for A,DFA*
    def BuildTable(self,Start,Goal):
	if(Start==[] or Goal==[]):
	    print("No start or goal given")
	    sys.exit(-1)
	print "BUILD TABLE"

    #Check if grid position is not blocked	
    def grid(self,x,y):
        if(x<0 or x>len(self.X) or y<0 or y>len(self.Y)):
	    #print ("LINE OF SIGHT::Out of Bounds")
	    #sys.exit(-2)
	    return False
        return self.ENV[y][x]==0

    #Check if position can have an edge
    def LineOfSight(self,s1,s2):
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

#Splitters would be:'-ENV-', 'NEXT LINE','-BLOCKS-', '-Start+Goal Pairs-'
def SplitList(List_of_All,Split):
    print "SPLIT BY:",Split
    if(Split!='-ENV-' and Split!='NEXT LINE' and Split!='-BLOCKS-' and Split!='-Start+Goal Pairs-'):
	print("Error, Enter Correct Splitter:Splitters would be:'-ENV-', 'NEXT LINE','-BLOCKS-', '-Start+Goal Pairs-'")
	sys.exit(-2)
    
    i = None
    k = 0
    #Get Pairs
    E3 = []
    for i in List_of_All:
	first = False
	if(i[0]==Split or Split=='-ENV-'):
	    j = None
	    for j in List_of_All[k:]:
		#
	        if(j[0]!='NEXT LINE' and j[0]!='-ENV-' and j[0]!='-BLOCKS-' and j[0] != '-Start+Goal Pairs-'):
		    E3.append(j)
		elif(j[0]=='NEXT LINE' and Split=='-BLOCKS-'):
		    E3.append(j)
		elif((j[0]=='NEXT LINE' and Split=='-ENV-')or (j[0]=='-BLOCKS-' and Split==j[0] and first)):
		    return E3
		first = True
	    break
    	k+=1
    return E3

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
    
    #GET ALL PAIRS OF TYPES
    E3 = SplitList(E2,'-Start+Goal Pairs-')
    #Got Start Goal Pairs
    StartGoalPairs = E3
    
    E3 = SplitList(E2,'-ENV-')
    #Got ENV:
    ENVS = E3
   
    E3 = SplitList(E2,'-BLOCKS-')
    #Got BLOCKS:
    Blocks = E3
    	
    print "StartGoalPairs:",StartGoalPairs,"\nENVS:",ENVS,"\nBLOCKS:",Blocks
    
    SGEN = StartEGen(Blocks,StartGoalPairs,ENVS)
 
    #return
   
    #M = mapMake(E2)
   
    return SGEN
if __name__=="__main__":
    main(sys.argv[:])
