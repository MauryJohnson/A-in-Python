#First run roscore
roscore &
#Run rosgazebo
ROBOT_INITIAL_POSE = "-x __ -y __" turtlebot_gazebo
#These use The Visibility graph
A

OR

FDA
#These use the graphs with 100*100 resolution, cost for neighboring nodes is now 0.01, heuristic to goal = heuristic/10
A_2D

OR

FDA_2D

#Example Run
#Have maps ready
roscore &
#This is if you want to start with world 1
ROBOT_INITIAL_POSE="-x -1 -y -1.75" roslaunch turtlebot_gazebo turtlebot_world.launch world_file:=$WORLD/world_1.world

python TestRun.py A map_1.txt -1 -1.75 -5 -1.75
OR
python TestRun.py FDA

the first command for TestRun starts robot starting at that map and position, and iterates through the rest of maps and positions.

the second command starts always at the first map and first position and iterates through the rest of maps and positions.
