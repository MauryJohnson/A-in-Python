import sys
sys.path.append("./ASTAR")
sys.path.append("./TBOTCLIENT")
sys.path.append("./ENVGEN")
import StartEGen
#Astar handles the path to map, and returns path seq
import Astar_Visibility_Graph
import DFAstar_Visibility_Graph
import Astar_2D_Array
import DFAstar_2D_Array
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
    global SState_Pid
    global SControl_Pid
    #Start RosGazebo Launch
    #R should be the entire ROSLAUNCH COMMAND
    p = Popen([R,''],stdin=PIPE,stdout=PIPE,stderr=PIPE,shell=True)
    p.wait()
    while p.poll() is None:
	line = p.stdout.readline()
	print line
    output,err = p.communicate("Input data passed to subprocess")
    rc = p.returncode
    #os.chdir(PrevDir)
    '''
    RGZ_Pid=-2
    SState_Pid.terminate()
    SState_Pid = -1
    SControl_Pid.terminate()
    SControl_Pid = -
    '''
    return output
    
def StartSrv():
    global SState_Pid
    global SControl_Pid
    #Start Servers not running
    if(SState_Pid<0):
	print("\nStarting State Server")
        SState_Pid = Process(target=S1)
	SState_Pid.daemon = True	
	SState_Pid.start()
	print("State Server PID:",SState_Pid)
    if(SControl_Pid<0):
	print("Starting Control Server")
	SControl_Pid = Process(target=S2)
	SControl_Pid.daemon = True
	SControl_Pid.start()
	print("Control Server PID:",SControl_Pid,"\n")

def StartGZB(R):
   global RGZ_Pid
   #Start Ros Gazebo
   if RGZ_Pid>=0:
       RGZ_Pid.terminate()
       RGZ_Pid = -1
   if RGZ_Pid<0:
        print("\nStart Ros-Gazebo")
        RGZ_Pid = Process(target=RGZ, args = [R,])
        RGZ_Pid.daemon = True	
        RGZ_Pid.start()
        print("Ros-Gazebo PID:",RGZ_Pid)

def A(Map,StartX,StartY,GoalX,GoalY):
    R = "python ASTAR/Astar.py"
    p = Popen([R,''],stdin=PIPE,stdout=PIPE,stderr=PIPE,shell=True)
    p.wait()
    while p.poll() is None:
	line = p.stdout.readline()
	print line
    output,err = p.communicate("Input data passed to subprocess")
    rc = p.returncode
    sys.exit(-1)    
def ASTAR(Map,Start,Goal):
    StartASTAR_Pid = -1
    print("\nStart ASTAR")
    try:StartASTAR_Pid = Process(target=A,args=[Map,Start[0],Start[1],Goal[0],Goal[1]])
    except:
	sys.exit(-1)
    StartASTAR_Pid.daemon = True
    StartASTAR_Pid.start()
    #StartASTAR_Pid.wait()
    print("FINISHED ASTAR")
	
def HD():
    #global RGZ_Pid
    global SState_Pid
    global SControl_Pid
    global PSeq
    global Goal_Found
    global H_Pid

    k = 0
    print("\nWaiting for Server EXIT\n")
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
    
        print "\nSERVER Status changed (BOT FAILURE?), Halt Program"
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
	else:
	    print "-------------HANDLER DETECTED NO GOAL FOUND-------------------"
        #H_Pid.terminate()
	sys.exit(-1)        
	H_Pid = -1
	#RGZ_Pid.terminate()
	#RGZ_Pid = -1
        

def Handler():
    global RGZ_Pid
    global H_Pid
    global SState_Pid
    global SControl_Pid

    if(H_Pid>=0):
	return
    #Runs Forever, until Server PID's Change back to <0
    print("\nStart Handler")
    print("Waiting for RosGazebo + Servers to Launch...")
    k = 0
    while(SState_Pid<0 and SControl_Pid<0):
	k = k
    H_Pid = Process(target=HD)
    H_Pid.daemon = True	
    H_Pid.start()
    print("Handler PID",H_Pid)

def main():
    global PSeq
    global Goal_Found
    global H_Pid

    StartSrv()
    
     #Handler()
	
    #H_Pid.join()

    #return
    MapPreference = ""
    StartPreference = []
    GoalPreference = []

    if((len(sys.argv[:])<2)):
        print("MUST ENTER Algorithm to run ''A'' or ''FDA'' ")
	sys.exit(-1)
    if(sys.argv[1]!="FDA" and sys.argv[1]!="A" and sys.argv[1]!="A_2D" and sys.argv[1]!="FDA_2D"):
	print("MUST ENTER Algorithm to run ''A'' or ''FDA'' ")
        sys.exit(-2)
    if(len(sys.argv[:])>2):
	#Third Argument will be map
	MapPreference = sys.argv[2]
	StartPreference = [(sys.argv[3]),(sys.argv[4])]
	GoalPreference = [(sys.argv[5]),(sys.argv[6])]
	print "Map Preferred:",MapPreference
	print "Start Pref:",StartPreference
	print "Goal Pref:",GoalPreference
	#return
	
    #else:
	#sys.exit(0)
    
    ARG = sys.argv[1]

    #WMaps ='$WORLD/'#'../turtlebot_simulator/turtlebot_gazebo/worlds/'#'~/catkin.ws/src/comprobfall2018-hw1/turtlebot_simulator/turtlebot_gazebo/worlds/' ##$WORLD/ #
    WMaps = ['$WORLD/','../turtlebot_simulator/turtlebot_gazebo/worlds/']
    #Maps = '$WORLD2/'#'../turtlebot_maps/'#'~/catkin.ws/src/comprobfall2018-hw1/turtlebot_maps/'#'$WORLD2/'#'
    Maps = ['$WORLD2/','../turtlebot_maps/']

    MapList = [['world_1.world','map_1.txt'],['world_2.world','map_2.txt'],['world_3.world','map_3.txt'],['world_4.world','map_4.txt'],['world_5.world','map_5.txt']]
    
    if(MapPreference not in [h[1] for h in MapList] and MapPreference !=""):
	print "Must Enter maps:"
	for k in MapList:
	    print k[1]
	return

    StartGoalList = []

    i = None
    j = None
    #Astar.main()
  
    #Command + "".join(CommandJ)+Command2+"".join(CommandJ2)+Command3+"".join(CommandJ3)

    Command = "(rosparam set goal_position ["   
    ###############################
    CommandJ = ["0",",","0","]"]
    #################################
    Command2 = " ; ROBOT_INITIAL_POSE=\"-x "
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

    ITER = 0

    for i in MapList:        
	print i
	#BUILD List of Start_Goals
		
	#SG = []
	Try_Map = False	
	if MapPreference!= "":
	    if MapPreference!=i[1]:
		print "Looking for MAP:",MapPreference,", Next Map..."
		#sys.exit(0)		
		continue
	SGEN =  StartEGen.main(Maps[1]+i[1])    
	H = []
	countSG = 0
	j = 0
	RunOnce = False	
	while j < len(SGEN.Start_Goals[:]):
	    #print j
	    if((j+1)%2==0):
		if(MapPreference!= ""):
		    if(float(SGEN.Start_Goals[j-1][0]) != float(StartPreference[0]) or float(SGEN.Start_Goals[j-1][1]) != float(StartPreference[1]) or float(SGEN.Start_Goals[j][0])!=float(GoalPreference[0]) or float(SGEN.Start_Goals[j][1])!=float(GoalPreference[1])   ):
			print("MY COORD::",StartPreference,GoalPreference,"Not Preferred: [%d,%d], Continue",(SGEN.Start_Goals[j-1],SGEN.Start_Goals[j]))
			ITER+=1			
			j+=1
			#sys.exit(-1)
		        continue
		    else:
			MapPreference = ""
			RunOnce = True		    


	        SG = [SGEN.Start_Goals[j-1],SGEN.Start_Goals[j]]
		ITER+=1
		SGEN.ADDSG(SG[0],SG[1])
			########################################################BUILDL MAP
		print ("\n\nFIRST GENERATE NEW GRAPH BASED ON START AND GOAL POSITIONS\n\n")


	   	#Set Goal Position prior
	    	CommandJ[0] = SG[1][0]
	    	CommandJ[2] = SG[1][1]
	    	#Set Up Start Pos for ROBOTPOSE
   	    	CommandJ2[0] = SG[0][0]
	    	CommandJ2[2] = SG[0][1]
	    	#Set World Map path
  	    	R = Command + "".join(CommandJ)#+Command2+"".join(CommandJ2)+Command3+WMaps[0]+i[0]+")"
	    	print "###########Start Command:#######",R
		if(MapPreference!=""):		
		    RGZ(R)
	    	#StartGZB(R) #- Start RosGazebo
		#StartSrv() #- Start Both Servers
	    	#Handler() #- First Waits until RosGazebo starts then Checks Both Servers



	        print "GOTO:",SG[0][0],SG[0][1],SG[1][0],SG[1][1], "MAP:",i
		#countSG= 0
		#Start A* or FDA*
	    	if(ARG=="A"):
		    #H = ASTAR([SGEN.Map],SG[0],SG[1])
		    H = Astar_Visibility_Graph.main([SGEN.Map,SG[0][0],SG[0][1],SG[1][0],SG[1][1],SGEN.ENV])	  
	    	elif(ARG=="FDA"):
		    #FDASTAR(SGEN.ENV,SG[0],SG[1])
		    H = DFAstar_Visibility_Graph.main([SGEN.Map,SG[0][0],SG[0][1],SG[1][0],SG[1][1],SGEN.ENV])      
		#)
		elif(ARG=="A_2D"):
		    H = Astar_2D_Array.main([SGEN.Map,SG[0][0],SG[0][1],SG[1][0],SG[1][1],SGEN.ENV])
	
		elif(ARG=="FDA_2D"):
		    H = DFAstar_2D_Array.main([SGEN.Map,SG[0][0],SG[0][1],SG[1][0],SG[1][1],SGEN.ENV])
		
		#if(ITER>=2 and ITER%2==0):
		    #return


		if(H!=None):
		    Goal_Found = True
		    for h in H:
			
		   	Where = Astar_Visibility_Graph.RequestClient()
	 		print("WHERE:",Where)
			h2 = [str(h[0]),str(h[1]),'0']
			print ("SEND:",h)
			Astar_Visibility_Graph.CommandClient(h2)		
		    
		     
		    PSeq = H
		    #H_Pid.join()

		
	    	SOLN[Sidx].append([i[1],H])
		if(MapPreference!=""):
		    MapPreference = ""
		    #break

		#countSG = 0		
		#SG = []
		#sys.exit(0)		
		j+=1	
		raw_input("Enter Anything To Continue (Make sure next position and map is set)")
		SGEN.DELETESG(SG[0],SG[1])	
		continue

	    #if(Sidx==3):
	    #sys.exit(0)
	    #################
	    #SG.append(j) 
	    print "#########IDX#########:",j
	    j+=1
	    #countSG+=1
	    #################
	Sidx+=1
	#if(RunOnce):
	    #break	
	#if(Sidx==2):
	    #sys.exit(-3)

    print("ALL SOLUTIONS:",SOLN)
	     
    SState_Pid.join()
    SControl_Pid.join()
    
    #print("Start")
    
if __name__=="__main__":
    main()
