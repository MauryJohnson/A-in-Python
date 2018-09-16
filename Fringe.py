#FRINGE

class Fringe():
    #Stack of [x,y] positions in ascending order by their corresp. G values
    def __init__(self):
	self.List = [] # [[y1,x1,f(1),py1,px1,g1],...,[yn,xn,f(n),pyn,pxn,g(n)]]
    
    #Insertion behaves like priority queue, compares F values
    def Insert(self,x):
        print("Ascending Inserting:",x)
    	
	if(x[2]<0):
	    print("F value is invalid")
	    return
	
	if(self.List == []):
	    self.List.append(x)
	    return
	i = None
	
	k = 0
	for i in (self.List):
	    #int j=0;
	    #for j in len(self.List[i]) and j <2:
	    #x, y, 
	    #print("I1")
	    #print(i[0].Coord[:],i[1])
	    #print("I2")
	    #print(g)
	    if(i[2]>x[2]):
	        self.List.insert(k,x)
	        return
	    k+=1
	#Append new state to end if it costs greater than all other costs
	self.List.append(x)
	return

    def Remove(self,x, y):
	print("Removing:[%d,%d]",x,y)
	#self.List.delete([x,y])
	#g = 0
    	#self.List.pop(self.List.index([x,y,g]))
        i = None
	for i in self.List:
	    if( i[0] == x and i[1] ==y ):
	 	self.List.pop(self.List.index(i))#[x,y,i[2]]))       
		print("Removed:[%d,%d]",x,y,i[2],)
		return
    
    def Pop(self):
	#Pop first node from fringe
	P = self.List.pop(0)
	print("Popping")
	print(P)
	return P
    
    def Print(self):
	print("Printing Fringe")
	print(self.List[:])
	return
    
    def ListInsert(self, L2, I):
	#self.List[I:I] = L2
	self.List.insert(I,L2)
	return
    def Exists(self,S):
	print("Does :",S," Exist?")
	for i in self.List:
	    #print("I:",i)
	    if(i[0]==S[0] and i[1]==S[1]):
		print("YES")
		return True
	print("NO")
	return False
