import sys

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