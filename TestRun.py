import sys
sys.path.append("./ASTAR")
sys.path.append("./TBOTCLIENT")
sys.path.append("./ENVGEN")
import StartEGen
#Astar handles the path to map, and returns path seq
import Astar
import DFAstar
import RunClient

import os
from subprocess import Popen, PIPE

def RunAstar():
    print("Run ASTAR")
    #Process
    #Return path sequence
def RunFDAstar():
    print ("run FDAstar")
    #Process
    #Return path sequence 

def main():
    if((len(sys.argv[:])<2)):
        print("MUST ENTER Algorithm to run ''A'' or ''FDA'' ")
	sys.exit(-1)
    if(sys.argv[1]!="FDA" and sys.argv[1]!="A"):
	print("MUST ENTER Algorithm to run ''A'' or ''FDA'' ")
        sys.exit(-2)

    ARG = sys.argv[1]

    WMaps ='../turtlebot_simulator/turtlebot_gazebo/worlds/'
    Maps = '../turtlebot_maps/'

    MapList = [[WMaps+'world_1.world',Maps+'map_1.txt'],[WMaps+'world_2.world',Maps+'map_2.txt'],[WMaps+'world_3.world',Maps+'map_3.txt'],[WMaps+'world_4.world',Maps+'map_4.txt'],[WMaps+'world_5.world',Maps+'map_5.txt']]
    
    StartGoalList = []

    i = None
    j = None
    #Astar.main()
    #Must call command to open a map

    #ROBOT_INITIAL_POSE="-x 2 -y 3" roslaunch turtlebot_gazebo turtlebot_world.launch world_file:=$WORLD/world_1.world

    SOLN = [['map_1'],['map_2'],['map_3'],['map_4'],['map_5']]
    Sidx = 0
    for i in MapList:
        print i
	#First Run Command to start env, then...
	SGEN =  StartEGen.main(i[1])
	#print("SGEN MAP:",SGEN.Map)
	SG = []
	H = []
	countSG = 0	
	for j in SGEN.Start_Goals[:]:
	    #print j
	    if(countSG==2):
		print "STOP:\n"
	        print "GOTO:",SG[0][0],SG[0][1],SG[1][0],SG[1][1], "MAP:",i
		countSG= 0
	    	if(ARG=="A"):
	            H = Astar.main([SGEN.Map,SG[0][0],SG[0][1],SG[1][0],SG[1][1]])
	    	else:
		    H = DFAstar.main([SGEN.Map,SG[0][0],SG[0][1],SG[1][0],SG[1][1]])
		#)
		
	    	#SOLN[Sidx].append([i[1],H])
		SG = []
		#sys.exit(0)		
		continue

	    #if(Sidx==3):
	    #sys.exit(0)
	    #################
	    SG.append(j) 
	    print "Add:",j
	    countSG+=1
	    #################
	Sidx+=1
	if(Sidx==2):
	    sys.exit(-3)

    print("ALL SOLUTIONS:",SOLN)
	     #rosparam set goal_position [j[2],j[3]]
	     #"ROBOT_INITIAL_POSE= ""-x "+str(j[0])+" -y "+str(j[1])+ 	""    +		"roslaunch turtlebot_gazebo turtlebot_world.launch 			world_file:=$WORLD/world_1.world"

	 #Call process Turtlebot Run for world_i...
	 #Gen ENV for map_i
	 #RunAstar()/RunFDAstar will command TBot to move at the end...
	 #Wait for Complete process and continue...
    #for i in MapList:
	#s = "


    #Must gen env based upon map i opened
    #Must wait for A* to return an answer given all coordinates x,y for map i
    #Must wait for FDA* to return an answer given all coordinates x,y for map i

        

    print("Start")
    
if __name__=="__main__":
    main()
