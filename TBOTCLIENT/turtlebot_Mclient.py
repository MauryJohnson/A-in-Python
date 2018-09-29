#!/usr/bin/env python

import sys
import rospy
#from turtlebot_ctrl.msg import TurtleBotState
from turtlebot_ctrl.srv import TurtleBotControl
from geometry_msgs.msg import Point
#from gazebo_msgs.srv import GetModelState
#from std_msgs.msg import Str
#class point:
   # def __init__(self):
    #    self.x = 0
#	self.y = 0
#	self.z = 0
 #   def update(self,x,y,z):
#	self.x = x
#	self.y = y
#	self.z = z

def callback(data):
    #print"I heard:[",data.x,",",data.y,"]","Goal reached? == ",data.goal_reached
    print " I heard:"#,data
    #rospy.loginfo("I heard",str(data))
    
def Coordinates(data):
    #print("Coordinates")
    rospy.init_node('RCoordinates')
    #P = Point(data[0],data[1],data[2])
    #P.point.x = data[0]
    #P.point.y = data[1]
    #P.point.z = data[2]
    #P.update(data[0],data[1],data[2])
    try:
        turtlebot_control = rospy.ServiceProxy("turtlebot_control",TurtleBotControl)
	resp1 = turtlebot_control(Point(data[0],data[1],data[2]))
	print "Response:",resp1
	return
    except rospy.ServiceException, e:
        print "Service call failed/BOT POSITION FAILURE??: %s"%e
	sys.exit(1)
    rospy.spin()
    #print("WAITING FOR: turtlebot_state")
    #rospy.wait_for_service('turtlebot_state')
    #try:
        #Coordinatess = rospy.Subscriber('turtlebot_state', TurtleBotState)
        #resp1 = Coordinatess
        #return resp1
    #except rospy.ServiceException, e:
        #print "Service call failed: %s"%e

def usage():
    return "%s MUST [x y,z]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 4:
        x = float(sys.argv[1])
        y = float(sys.argv[2])
	z = float(sys.argv[3])
    else:
        print usage()
        sys.exit(1)
    print "Requesting COORDINATES [%s,%s,%s]"%(x, y, z)
    #print (Coordinates())
    Coordinates([x,y,z])
