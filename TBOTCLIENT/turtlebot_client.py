#!/usr/bin/env python

import sys
import rospy
from turtlebot_ctrl.msg import TurtleBotState
from gazebo_msgs.srv import GetModelState
from std_msgs.msg import String

def callback(data):
    print"I heard:[",data.x,",",data.y,"]","Goal reached? == ",data.goal_reached
    #rospy.loginfo("I heard",str(data))
    
def Coordinates():
    print("Initialize Coordinates")
    rospy.init_node('Coordinates')
    rospy.Subscriber("turtlebot_state",TurtleBotState,callback)
    rospy.spin()
    #print("WAITING FOR: turtlebot_state")
    #rospy.wait_for_service('turtlebot_state')
    #try:
        #Coordinatess = rospy.Subscriber('turtlebot_state', TurtleBotState)
        #resp1 = Coordinatess
        #return resp1
    #except rospy.ServiceException, e:
        #print "Service call failed: %s"%e

#def usage():
    #return "%s MUST [x y]"%sys.argv[0]

if __name__ == "__main__":
    #if len(sys.argv) == 3:
        #x = (sys.argv[1])
        #y = (sys.argv[2])
    #else:
        #print usage()
        #sys.exit(1)
    #print "Requesting COORDINATES [%s,%s]"%(x, y)
    print (Coordinates())
