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
print("Current DIR:",os.getcwd())
from subprocess import Popen, PIPE
from multiprocessing import Process

SControl_Pid = -1
SState_Pid = -1

RGZ_Pid = -1

H_Pid = -1

#Indicators
Goal_Found = False
PSeq = []

def S1():
    global SState_Pid
    #Start State Server
    PrevDir = os.getcwd()
    os.chdir("../turtlebot/turtlebot_ctrl/scripts")
    p = Popen(['python turtlebot_state.py',''],stdin=PIPE,stdout=PIPE,stderr=PIPE,shell=True)
    output,err = p.communicate("Input data passed to subprocess")
    rc = p.returncode
    os.chdir(PrevDir)
    SState_Pid = -2
    return output

def S2():
    global SControl_Pid
    #Start Control Server
    PrevDir = os.getcwd()
    os.chdir("../turtlebot/turtlebot_ctrl/scripts")
    p = Popen(['python turtlebot_control.py',''],stdin=PIPE,stdout=PIPE,stderr=PIPE,shell=True)
    output,err = p.communicate("Input data passed to subprocess")
    rc = p.returncode
    os.chdir(PrevDir)
    SControl_Pid=-2
    return output

def RGZ(R):
    global RGZ_Pid
    #Start RosGazebo Launch
    #R should be the entire ROSLAUNCH COMMAND
    p = Popen([R,''],stdin=PIPE,stdout=PIPE,stderr=PIPE,shell=True)
    output,err = p.communicate("Input data passed to subprocess")
    rc = p.returncode
    #os.chdir(PrevDir)
    RGZ_Pid=-2
    return output
    
def StartSrv():
    global SState_Pid
    global SControl_Pid
    #Start Servers not running
    if(SState_Pid<0):
	print("Starting State Server")
        SState_Pid = Process(target=S1)
	SState_Pid.daemon = True	
	SState_Pid.start()
	print("State Server PID:",SState_Pid)
    if(SControl_Pid<0):
	print("Starting Control Server")
	SControl_Pid = Process(target=S2)
	SControl_Pid.daemon = True
	SControl_Pid.start()
	print("Control Server PID:",SControl_Pid)

def StartGZB(R):
   global RGZ_Pid
   #Start Ros Gazebo
   if RGZ_Pid>=0:
       RGZ_Pid.terminate()
       RGZ_Pid = -1
   if RGZ_Pid<0:
        print("Start Ros-Gazebo")
        RGZ_Pid = Process(target=RGZ, args = [R,])
        RGZ_Pid.daemon = True	
        RGZ_Pid.start()
        print("Ros-Gazebo PID:",RGZ_Pid)
	   
def HD():
    #global RGZ_Pid
    global SState_Pid
    global SControl_Pid
    global PSeq
    global Goal_Found
    global H_Pid

    k = 0
    print("Waiting for Server EXIT")
    while(SControl_Pid>=0 and SState_Pid>=0):
	if(Goal_Found):
	    #Goal Found, PSeq is not empty
	    for i in PSeq:	
		#Iterate through all moves, wait for server to respond
		IN = Astar.RequestClient()
		print "WHERE:",IN
		OUT = Astar.CommandClient(i)
		print "COMMAND OUTPUT:",OUT
 	    Goal_Found = False
	    PSeq = []
	#Continuing until these change
    print "SERVER Status changed, Halt Program"
    H_Pid.terminate()
    H_Pid = -1
    sys.exit(-1)

def Handler():
    global RGZ_Pid
    global H_Pid
    if(H_Pid>=0):
	return
    #Runs Forever, until Server PID's Change back to <0
    print("Start Handler")
    print("Waiting for RosGazebo to Launch...")
    while(RGZ_Pid<0):
	k = k
    H_Pid = Process(target=HD)
    H_Pid.daemon = True	
    H_Pid.start()
    print("Handler PID",H_Pid)

def main():
    global PSeq
    global Goal_Found

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
  
    #Command + "".join(CommandJ)+Command2+"".join(CommandJ2)+Command3+"".join(CommandJ3)

    Command = "roscore | rosparam set goal_position ["   
    ###############################
    CommandJ = ["0",",","0","]"]
    #################################
    Command2 = " && ROBOT_INITIAL_POSE=\"-x "
    #################################
    CommandJ2 = ["0"," -y ","0","\""]
    ###################################
    Command3 = " roslaunch turtlebot_gazebo turtlebot_world.launch world_file:="
    #####################################
    #CommandJ3 = [WMaps,"W"]
    ######################################
   
    #CTOT = Command + "".join(CommandJ)+Command2+"".join(CommandJ2)+Command3+"".join(CommandJ3)
    #print "TEST COMMAND:",CTOT
    #return
    #COMMAND rosparam set goal_position [x,y]
    
    #ROBOT_INITIAL_POSE="-x 2 -y 3" roslaunch turtlebot_gazebo turtlebot_world.launch world_file:=$WORLD/world_1.world
    #StartSrv()
    #If State process is killed, robot failed, exit program or continue?
    #If continue, then Kill Rosgazebo and restart.. Call Func StartRosGazebo():
    
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
	    StartSrv() #- Start Both Servers
	    #print j
	    if(countSG==2):
		#print "STOP:\n"
		#Set Goal Position prior
	    	CommandJ[0] = SG[1][0]
	    	CommandJ[2] = SG[1][1]
	    	#Set Up Start Pos for ROBOTPOSE
   	    	CommandJ2[0] = SG[0][0]
	    	CommandJ2[2] = SG[0][1]
	    	#Set World Map path num
	    	#CommandJ3[1] = i[1]
  	    	R = Command + "".join(CommandJ)+Command2+"".join(CommandJ2)+Command3+i[0]
	    	print "Start Command:",R
	    	StartGZB(R) #- Start RosGazebo
	    	Handler() #- First Waits until RosGazebo starts then Checks Both Servers
	        print "GOTO:",SG[0][0],SG[0][1],SG[1][0],SG[1][1], "MAP:",i
		countSG= 0
	    	if(ARG=="A"):
	            H = Astar.main([SGEN.Map,SG[0][0],SG[0][1],SG[1][0],SG[1][1]])
	    	else:
		    H = DFAstar.main([SGEN.Map,SG[0][0],SG[0][1],SG[1][0],SG[1][1]])
		#)
		if(H!=None):
		    Goal_Found = True
		    PSeq = H
	    	SOLN[Sidx].append([i[1],H])
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
	#if(Sidx==2):
	    #sys.exit(-3)

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
