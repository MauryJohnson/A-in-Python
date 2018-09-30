import sys
from fractions import gcd

def plotlinelow(mapfull, x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    yi = 1
    if dy < 0:
        yi = -1
        dy = -dy
    D = 2*dy - dx
    y = y0

    for x in range(x0, x1):
<<<<<<< HEAD
        for y2 in range(y-19, y+19):
            mapfull[x][y2] = 0
=======
        mapfull[x][y] = 0
>>>>>>> 2a9d016... EVERYTHING_EXCEPT_SERVER_AND_FDA_CONFIGURED(90%)
        if D > 0:
            y += yi
            D -= 2*dx
        D += 2*dy
    
def plotlinehigh(mapfull, x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    xi = 1
    if dx < 0:
        xi = -1
        dx = -dx
    D = 2*dx - dy
    x = x0

    for y in range(y0, y1):
<<<<<<< HEAD
        for x2 in range(x-19, x+19):
            mapfull[x2][y] = 0
=======
        mapfull[x][y] = 0
>>>>>>> 2a9d016... EVERYTHING_EXCEPT_SERVER_AND_FDA_CONFIGURED(90%)
        if D > 0:
            x += xi
            D -= 2*dy
        D += 2*dx

def plotline(mapfull, x0, y0, x1, y1):
    if abs(y1-y0) < abs(x1-x0):
        if x0 > x1:
            plotlinelow(mapfull, x1, y1, x0, y0)
        else:
            plotlinelow(mapfull, x0, y0, x1, y1)
    else:
        if y0 > y1:
            plotlinehigh(mapfull, x1, y1, x0, y0)
        else:
            plotlinehigh(mapfull, x0, y0, x1, y1)

def mapMake(mapList):

    size = (int(mapList[1][0]) - int(mapList[1][1])) * 100

    obstacles = []
    index = mapList.index(['-BLOCKS-']) + 1

    temp = []
    while(not mapList[index][0] == '-BLOCKS-'):
        index += 1
        while(not (mapList[index][0] == 'NEXT LINE' or mapList[index][0] == '-BLOCKS-')):
            print mapList[index], mapList[index][0], mapList[index][0] == 'NEXT LINE'
            temp.append((float(mapList[index][0]), float(mapList[index][1])))
            index += 1
        obstacles.append(temp)
        temp = []
    
    print obstacles
    for item in obstacles:
        print item

    mapfull = []

    for x in range(0, size):
        temp = []
        for y in range(0, size):
            if x < 20 or x > size - 20 or y < 20 or y > size - 20:
                temp.append(0)
            else:
                temp.append(1)
        mapfull.append(temp)
    
    for obstacle in obstacles:
        obslen = len(obstacle)
        for i in range(0, obslen):
            point = obstacle[i]
            point2 = obstacle[(i+1)%obslen]
<<<<<<< HEAD

            for x in range(int(point[0] * 100) + size/2 - 19, int(point[0] * 100) + size/2 + 19):
                for y in range(int(point[1] * 100) + size/2 - 19, int(point[1] * 100) + size/2 + 19):
                    mapfull[x][y] = 0
            
            plotline(mapfull, int(point[0] * 100) + size/2, int(point[1] * 100) + size/2, int(point2[0] * 100) + size/2, int(point2[1] * 100) + size/2)
    
    f = open("Maze", 'w')
    for line in mapfull:
        for char in line:
            f.write(str(char) + " ")
        f.write('\n')

    return mapfull
                
=======
            
            plotline(mapfull, int(point[0] * 100), int(point[1] * 100), int(point2[0] * 100), int(point2[1] * 100))
    
    return mapfull
>>>>>>> 2a9d016... EVERYTHING_EXCEPT_SERVER_AND_FDA_CONFIGURED(90%)
