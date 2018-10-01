from EnvGen import EnvGen
from MapMake import mapMake
import math
import sys
#from Astar import Execute
from subprocess import Popen, PIPE

#ENV CAN EVEN JUST BE LIST OF ALL BLOCKS AND THEIR AREAS
#Also Get 
#ENV = []
#EnvTable = []

class StartEGen():   
    def __init__(self,VL,SG,ENVS):
	self.EnvTable = []
 	self.ENV = []
	#self.Borders = []
	self.Y = -1
	self.X = -1
	self.MidY = -1
	self.MidX = -1
 	self.Map = []
	#Should only keep track of the next start goal pair to use
	self.Start_Goals = SG
	self.Vertex_List = VL
	#Generate entire 2D ENV WITH BLOCKS
	#self.ENV = mapMake 	
	
	#self.GenEnv(ENVS,VL)
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

    def PCheck(self,MaxEnvYX,Pairs,i):
	if Pairs[0][0]!='NEXT LINE':
	    D = self.Distance(Pairs)
	    print "Distance:",D
	    if i%2==1:
		if(D>MaxEnvYX[0]):
		    MaxEnvYX[0] = D	
	    else:
		if(D>MaxEnvYX[1]):
		    MaxEnvYX[1] = D
    #def Exec(self,E):
	#Execute(
    def ValidPoint(self,MyPoint):
	print("Validate point")
	i = 0
	k = 0
	
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

	A_Star_Points = []

	print ""
	while i<len(ENVS):
	    if(len(Pairs)>=2):
		print "ENV PAirs",Pairs

		#TRACE ASTAR################
		A_Star_Points.append(Pairs)

		self.PCheck(MaxEnvYX,Pairs,i)
		print "MAX ENV:",MaxEnvYX
		i-=1
		Pairs = []
		continue
	    else:
		Pairs.append(ENVS[i])
	        i+=1
		continue
	print "SECOND TO FINAL ENV PAirs",Pairs
	
	#TRACE ASTAR################
	A_Star_Points.append(Pairs)

	self.PCheck(MaxEnvYX,Pairs,i)
	#Check first and last pairs
	Pairs = []
	Pairs.append(ENVS[0])
	Pairs.append(ENVS[i-1])
	print "FINAL ENV PAirs",Pairs

	#TRACE ASTAR################
	A_Star_Points.append(Pairs)
	
	self.PCheck(MaxEnvYX,Pairs,i-1)

	print "MAX ENV LENGTHS:",MaxEnvYX
	#GET MIDPOINTS
	self.Y = int(MaxEnvYX[0]*100)
	self.MidY = int((MaxEnvYX[0]*100)/2)
	self.X = int(MaxEnvYX[1]*100)
	self.MidX = int((MaxEnvYX[1]*100)/2)
	print "MIDPOINT Y,X:[%d,%d]"%(self.MidY,self.MidX)

	i = 0
	k = 0

	#SET ENV
	for i in range(self.Y):
	    X_DIRECTION = []
	    k = 0
	    for k in range(self.X):
		if(i==0 or i ==(self.Y)-1):
		    X_DIRECTION.append(0)
		else:
		    X_DIRECTION.append(1)
	    X_DIRECTION[0] = 0
	    X_DIRECTION[k] = 0
	    self.ENV.append(X_DIRECTION)
	#print "ENV:", self.ENV
	#HAVE ENV WITH ALL ZEROES        
	#sys.exit(0)
	#FOR BUILD ENV...
	print "SIZE:%d,%d"%(i,k)
	#Border = [[0,0],[i,0],[i,k],[0,k]]	
	#Pairs = []
	
	# CREATE THE PROCESS
	#print("\nStart Ros-Gazebo")
        #RGZ_Pid = Process(target=RGZ, args = [R,])
        #RGZ_Pid.daemon = True	
        #RGZ_Pid.start()
        #print("Ros-Gazebo PID:",RGZ_Pid)

	#Execute(self.ENV,i,k,0,k)
	#Execute(self.ENV,0,k,0,0)
	#Execute(self.ENV,0,0,i,0)
	#sExecute(self.ENV,i,0,i,k)
	

	#i = 2*self.MidY-1	
	#while i>=0:
	    #self.ENV[i][0] = 0
	    #i-=1
	
	print self.ENV
	print "LEAVEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE"
	#sys.exit(0)
	A_Star_Points = []
	Pairs = []
	i = 0
	#K gets last neighbor for last object
	k = 0
	NLine  =False
	MaxVtexYX = [-sys.maxint,-sys.maxint]
	while i<len(VtexList):
	    if(len(Pairs)>=2):
		if(Pairs[1][0]=='NEXT LINE'):
		    Pairs[0]=['NEXT LINE']
		    #k+=1
		print "BLOCK PAirs",Pairs
		self.PCheck(MaxVtexYX,Pairs,i)

		#TRACE ASTAR################

		i-=1
		Pairs = []
		NLine = False
		continue
	    else:
		if(VtexList[i][0]=='NEXT LINE' or NLine):
		    Pairs.append(['NEXT LINE'])
		    #Pairs.append(['NEXT LINE'])	
		    NLine = True
		    k=i
		    i+=1
		    continue	
		else:		
		    Pairs.append(VtexList[i])
	        i+=1
		continue
	print "2nd to FINAL BLOCK PAirs",Pairs
	
	#TRACE ASTAR################

	self.PCheck(MaxVtexYX,Pairs,i)
	#Check first and last pairs
	Pairs = []
	Pairs.append(VtexList[k])
	Pairs.append(VtexList[i-1])
	print "FINAL BLOCK PAirs",Pairs


	
	

	#TRACE ASTAR################

	self.PCheck(MaxVtexYX,Pairs,i-1)

	#self.Borders = 

	#print "Max Vtex:",MaxVtexYX
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
  	#print self.EnvTable

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
    
    #sys.exit(-1)
    return SGEN
if __name__=="__main__":
    main(sys.argv[:])
