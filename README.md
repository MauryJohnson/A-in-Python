A* Search Algorithm

python StartEGen.py map_5.txt
Returns points labelling what the coordinates are.
requires StartEGen.py and EnvGen.py

???python EnvCreator ??? - NOT CREATED YET - Creates environment Given details from abocve - fills in outlines of the entire environment and all of the obstacles

python Astar.py 0.1 0.1 0.2 0.2 -> 10 10 20 20
will travel to coordinates (0.2,0.2) from (0.1,0.1) -> 10,10 20,20 are the coordinates in the increased graph size (multiply by 100)

#######Process HANDLING
Run a process handles for the servers
Check if servers shut down because of robot or because started new rosgazebo process
if server shut down because robot, exit
if server shut down because of rosgezebo restart, start server again
Every time rosgazebo starts, server must start
