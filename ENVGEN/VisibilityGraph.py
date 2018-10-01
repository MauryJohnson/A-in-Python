from math import sqrt

staggermod = 0

def toArrcoord(n):
    return int(float(n) * 100) + staggermod

def toRealcoord(n):
    return float(n - staggermod) / 100

def addStartGoal(visibilityGraph, mapfull, start, goal):
    if lineOfSight(mapfull, (toArrcoord(start[0]),toArrcoord(start[1])), goal):
        cost = distance(start, goal)
        visibilityGraph[start] = [goal, cost]
        visibilityGraph[goal] = [start, cost]
        return visibilityGraph
    visibilityGraph[start] = []
    for key in visibilityGraph.keys():
        if start[0] == key[0] and start[1] == key[1]:
            continue
        print "New tentative connection ", (start, key)
        if lineOfSight(mapfull, (toArrcoord(start[0]), toArrcoord(start[1])), (toArrcoord(key[0]), toArrcoord(key[1]))):
            print "New connection ", (start, key)
            cost = distance(start, key)
            visibilityGraph[start].append((key, cost))
            visibilityGraph[key].append((start, cost))
    visibilityGraph[goal] = []
    for key in visibilityGraph.keys():
        if goal[0] == key[0] and goal[1] == key[1]:
            continue
        print "New tentative connection ", (goal, key)
        if lineOfSight(mapfull, (toArrcoord(goal[0]), toArrcoord(goal[1])), (toArrcoord(key[0]), toArrcoord(key[1]))):
            print "New connection ", (goal, key)
            cost = distance(goal, key)
            visibilityGraph[goal].append((key, cost))
            visibilityGraph[key].append((goal, cost))

def deleteStartGoal(visibilityGraph, start, goal):
    for item in visibilityGraph[start]:
        visibilityGraph[item[0]].remove((start, item[1]))
    del visibilityGraph[start]
    for item in visibilityGraph[goal]:
        visibilityGraph[item[0]].remove((goal, item[1]))
    del visibilityGraph[goal]

# def checklinelow(mapfull, x0, y0, x1, y1):
#     dx = x1 - x0
#     dy = y1 - y0
#     yi = 1
#     if dy < 0:
#         yi = -1
#         dy = -dy
#     D = 2*dy - dx
#     y = y0

#     for x in range(x0, x1):
#         for y2 in range(y-19, y+19):
#             if mapfull[x][y2] == 0:
#                 return False
#         if D > 0:
#             y += yi
#             D -= 2*dx
#         D += 2*dy
    
#     return True

def lineOfSight(mapfull, node1, node2):
 
    x0 = node1[0]
    y0 = node1[1]
    x1 = node2[0]
    y1 = node2[1]
 
    f = 0
    dy = y1 - y0
    dx = x1 - x0

    sy = 1
    sx = 1

    if dy < 0:
        dy = -dy
        sy = -1    
    if dx < 0:
        dx = -dx
        sx = -1

    if dx >= dy:
        while x0 !=  x1:
            f += dy
            if f >= dx:
                if mapfull[x0 + ((sx - 1)/2)][y0 + ((sy - 1)/2)]==0:
                    return False
                y0 += sy
                f -= dx
            if f != 0 and mapfull[x0 +((sx-1)/2)][y0 + ((sy-1)/2)]==0:
                return False
            if dy == 0 and mapfull[x0 + ((sx - 1)/2)][y0]==0 and mapfull[x0 + ((sx - 1)/2)][y0 - 1]==0:
                return False
            x0 += sx
    else:
        while y0 != y1:
            f += dx
            if f >= dy:
                if mapfull[x0 + ((sx - 1)/2)][y0 + ((sy - 1)/2)]==0:
                    return False
                x0 += sx
                f -= dy
            if f != 0 and mapfull[x0 + ((sx - 1)/2)][y0 + ((sy - 1)/2)]==0:
                return False
            if dx == 0 and mapfull[x0][y0 + ((sy - 1)/2)]==0 and mapfull[x0 - 1][y0 + ((sy - 1)/2)][y0 - 1]==0:
                return False
            y0 += sy
    return True

def distance(node1, node2):
    return sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)

# def checklinehigh(mapfull, x0, y0, x1, y1):
#     dx = x1 - x0
#     dy = y1 - y0
#     xi = 1
#     if dx < 0:
#         xi = -1
#         dx = -dx
#     D = 2*dx - dy
#     x = x0

#     for y in range(y0, y1):
#         for x2 in range(x-19, x+19):
#             if mapfull[x2][y] == 0:
#                 return False
#         if D > 0:
#             x += xi
#             D -= 2*dy
#         D += 2*dx
    
#     return True

# def lineOfSight(mapfull, x0, y0, x1, y1):
#     if abs(y1-y0) < abs(x1-x0):
#         if x0 > x1:
#             return checklinelow(mapfull, x1, y1, x0, y0)
#         else:
#             return checklinelow(mapfull, x0, y0, x1, y1)
#     else:
#         if y0 > y1:
#             return checklinehigh(mapfull, x1, y1, x0, y0)
#         else:
#             return checklinehigh(mapfull, x0, y0, x1, y1)

def isCorner(mapfull, x, y):
    if mapfull[x-1][y] == 0 and mapfull[x-1][y-1] == 0 and mapfull[x][y-1] == 0 and mapfull[x+1][y-1] == 1 and mapfull[x+1][y] == 1 and mapfull[x+1][y+1] == 1 and mapfull[x][y+1] == 1 and mapfull[x-1][y+1] == 1:
        return True
    if mapfull[x-1][y] == 1 and mapfull[x-1][y-1] == 1 and mapfull[x][y-1] == 0 and mapfull[x+1][y-1] == 0 and mapfull[x+1][y] == 0 and mapfull[x+1][y+1] == 1 and mapfull[x][y+1] == 1 and mapfull[x-1][y+1] == 1:
        return True
    if mapfull[x-1][y] == 1 and mapfull[x-1][y-1] == 1 and mapfull[x][y-1] == 1 and mapfull[x+1][y-1] == 1 and mapfull[x+1][y] == 0 and mapfull[x+1][y+1] == 0 and mapfull[x][y+1] == 0 and mapfull[x-1][y+1] == 1:
        return True
    if mapfull[x-1][y] == 0 and mapfull[x-1][y-1] == 1 and mapfull[x][y-1] == 1 and mapfull[x+1][y-1] == 1 and mapfull[x+1][y] == 1 and mapfull[x+1][y+1] == 1 and mapfull[x][y+1] == 0 and mapfull[x-1][y+1] == 0:
        return True
    return False

def computeGraphNodes(mapList, mapfull):
    global staggermod

    size = (int(mapList[1][0]) - int(mapList[1][1]) + 1) * 100
    staggermod = -(int(mapList[1][1])) * 100

    print size
    print staggermod

    rawnodes = []
    index = mapList.index(['-BLOCKS-']) + 1

    while(not mapList[index][0] == '-BLOCKS-'):
        index += 1
        if(not (mapList[index][0] == 'NEXT LINE' or mapList[index][0] == '-BLOCKS-')):
            print mapList[index], mapList[index][0], mapList[index][0] == 'NEXT LINE',
            rawnodes.append((toArrcoord(mapList[index][0]), toArrcoord(mapList[index][1])))
    
    nodes = []
    for node in rawnodes:
        # x - 19, x + 19, y - 19, y + 19
        x = node[0]
        y = node[1]
        if isCorner(mapfull, x-19, y-19):
            nodes.append((x-20, y-20))
        if isCorner(mapfull, x-19, y+19):
            nodes.append((x-20, y+20))
        if isCorner(mapfull, x+19, y+19):
            nodes.append((x+20, y+20))
        if isCorner(mapfull, x+19, y-19):
            nodes.append((x+20, y-20))
    
    max = toArrcoord(mapList[1][0])-20
    min = toArrcoord(mapList[1][1])+20
    nodes.append((max, max))
    nodes.append((max, min))
    nodes.append((min, min))
    nodes.append((min, max))
    return nodes

def connectGraph(mapfull, nodes):
    visibilityGraph = {}

    for node in nodes:
        nodereal = (toRealcoord(node[0]), toRealcoord(node[1]))
        try:
            if visibilityGraph[nodereal] == None:
                visibilityGraph[nodereal] = []
        except:
            visibilityGraph[nodereal] = []
            print "New node iteration"
        for node2 in nodes:
            if node[0] == node2[0] and node[1] == node2[1]:
                continue
            node2real = (toRealcoord(node2[0]), toRealcoord(node2[1]))
            try:
                if nodereal in visibilityGraph[node2real]:
                    continue
                else:
                    pass
            except:
                visibilityGraph[node2real] = []
            print "New tentative connection ", (nodereal, node2real)
            if lineOfSight(mapfull, node, node2):
                print "New connection ", (nodereal, node2real)
                cost = distance(nodereal, node2real)
                visibilityGraph[nodereal].append((node2real, cost))
                visibilityGraph[node2real].append((nodereal, cost))
    print visibilityGraph
    return visibilityGraph

def computeVisibilityGraph(maplist, mapfull):
    return connectGraph(mapfull, computeGraphNodes(maplist,mapfull))