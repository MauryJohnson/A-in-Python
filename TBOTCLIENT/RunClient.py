import sys
import re
#import os
from subprocess import Popen, PIPE

#Create a process for each command type with return information
def main():
    #If No argument given, run INFO receiver client
    if(len(sys.argv[:])==1):
	#create = [sys.executable, 'turtlebot_client.py']
	print("Run turtlebot_client.py")
	#subprocess.check_output(create)
	p1 = Popen(['python ./turtlebot_client.py',' '],stdin=PIPE,stdout=PIPE,stderr=PIPE,shell=True)
	output, err = p1.communicate("Input data passed to subprocess")
	rc = p1.returncode
	print "Return Code:",rc,output
	O = output.split(",")
        O = "".join(O)
  	O = re.sub(' +','',O)
	O = re.sub("\nNone\n","",O)
	O = O.split("data:")	
        O.pop(0);
	print "List:",O
	#RUN RECEIVE CLIENT
    #If Given arguments, run command robot client
    else:
	if(len(sys.argv[:])<4):
	    print("MUST ENTER X,Y,Z ARGUMENTS TO COMMAND ROBOT")
	    sys.exit(-2) 
	#create2 = [sys.executable, 'turtlebot_Mclient.py']
	print("Run turtlebot_Mclient.py")	
	p2 = Popen(['python ./turtlebot_Mclient.py'+ ' '+ sys.argv[1] + ' ' + sys.argv[2] + ' ' + sys.argv[3]],stdin=PIPE,stdout=PIPE,stderr=PIPE,shell=True)
	output, err = p2.communicate("Input data passed to subprocess")
	rc = p2.returncode
	print "Return Code:",rc,output
	#RUN COMMAND CLIENT
if __name__=="__main__":
    main()
