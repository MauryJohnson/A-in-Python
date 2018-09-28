#Env Gen Class
from __future__ import print_function
import functools
from numpy import loadtxt
import re
import sys

class EnvGen():

    def __init__(self):
	#Consists of total env naive of subset env
	#Area will be max()*max() first	
 	self.FullENV = []
	
	#Consists of the subset env 
	self.SubENV = []
 	self.IntersectENV  =[]

    def is_int(self,n):
    #b = False
        try:
            int(n)
            return True
        except ValueError:
            return False
    
    def is_float(self,n):
    #b = False
        try:
            float(n)
            return True
        except ValueError:
            return False
    def AddLists(self,A,X):
	if(A==[]):
	    A.append(sys.maxint)
	    A.append(sys.maxint)
	#if(B==[]):
	    #B.append(sys.maxint)
	    #B.append(sys.maxint)
	    #return
	if(A[0]!=sys.maxint and A[1]!=sys.maxint): #and B[0]!= sys.maxint and B[1]!= sys.maxint):
	    print("ALL POINTS SATISFIED",end = "\n")
	    return
	if(A[0]==sys.maxint):
	    print("ADD A1")
	    A[0] = X
	    return
	if(A[1]==sys.maxint):
	    print("ADD A2")
	    A[1] = X
	    return
	#if(B[0]==sys.maxint):
	 #   print("ADD B1")
	  #  B[0] = X
	   # return
        #if(B[1]==sys.maxint):	
	 #   print("ADD B2")
	  #  B[1] = X
	   # return
    def FixBuff(self,E):
	i = ''
	k = 0
	j = 0
	#Check if find new line as first char
	for i in E:
	    if(len(i)==0):
		#E.pop(k)
		#k-=1
		continue
	    if(i[0]=="\n"):
	        print("Found Badly Formatted Culprit:",i,end = "\n")
		#Remove previous index and merge the two 
		if(k>0):
		    s = ""+E[k-1]
		    s+=""+i
		    s.replace(" ","")
		    g = ""+E[k]
		    E[k] = s
		    print("POPPING:",E[k-1],"Fixed Str:",s,end = "\n")
		    E.pop(k-1)
		    #if(E[k+1]==g):
			#E.pop(k+1)
		    
		else:
		    print("ERROR, Cannot Fix BAD FORMAT",end = "\n") 
		    sys.exit(-2)
	
		
	    #while(j<len(i)):
		
		
		#j+=1
	    k+=1
    def CreateENV(self,m):
	printf = functools.partial
	#f = open('m','r')
	f = open(m,'r')    	
	x = f.read()#.split('\n')
	#x = ''.join(x)
    	#f.close()
    	print ("Array")
    	#x.replace(")  ", ") ")
	#x = ' '.join(x.split(" "))
	x= re.sub(' +', ' ', x)
	print (x)
	
	#x.replace('  ',' ')


	y = re.split(r'()',x)
	#y.replace("  "," ")
	sub = ''
	#for sub in y:
	y = [s.translate(None, "()#") for s in y]
	y = ''.join(y)
	#y.replace('  \n','\n')
	y = re.split(' ',y)
	g = ','.join(y).replace('---','')
	#g.replace(' \n','HERE')
	M = g.split(',')
	self.FixBuff(M)
	m = ''
	for m in M:
	    if(len(m)==0):
		continue
	    if(m[0]=='\n'):
		M.remove(m)
	#M = [s.translate(None, " ") for s in M]
	#M.replace(' \n','\n')
	#M.split(',')
	#M = [s.translate(None, "\n") for s in M]
	print(M)
	#if(len(M)%2!=0):
	    #print("Error Parsing",end="\n")
	    #sys.exit(-1)	
	#Distances between each point, for first case will have four
	D = []
	EE = []
	#Point 1	
	L1 = []
	#Point 2
	L2 = []
	self.AddLists(L1,sys.maxint)
	type = 0

	Lines = 0

	i = None
	j = ''
	#B = True
	print("PARSE M",end = "\n")
	pairs = 0	
	L1 = []	
	for i in M:
	    #L1 = []
	    #L2 = []
	    s = ""
	    #if(i.count('\n')==1):
	    Lines = i.count('\n')
	    if(Lines>0):
		L2 = (''.join(i).split('\n'))#split('')
		print("Strings With New Lines:",L2[1:])
	
		if(self.is_float(L2[0]) or self.is_int(L2[0])):
		    self.AddLists(L1,L2[0]) 
		    EE.append(L1)
		    L1 = []

		pairs2 = 0
		g = None
		j = ''
		s2 = ""
		if(pairs2==0):
                    print("(",end="")
		for g in L2[1:]:
		    Lines2 = g.count('\n')
		    for j in g:
			print(j,end="")
			s2+=j
		    if(pairs2==0 and (self.is_float(s2) or self.is_int(s2))):
		        print(",",end="")
		        if(self.is_float(s2) or self.is_int(s2)):
		            self.AddLists(L1,s2)        
		        pairs2+=1
	            elif(pairs2==1):
	                print(")",end="")
		        if(self.is_float(s) or self.is_int(s2)):
		            self.AddLists(L1,s2)
		            EE.append(L1)
		        L1 = []		
		        pairs2=0
	            if Lines==2:
	                print("",end = "\n")
			if(type==0):
			    EE.append(['-ENV-'])
			    type+=1
			elif(type==1 or type==2):
			    EE.append(['-BLOCKS-'])
			    type+=1
			    #if(type==2):
			        #EE.append(['-Start+Goal Pairs-'])	    	
			else:
			    EE.append(['-Start+Goal Pairs-']) 
	        continue
	    #pairs = 0	

	    if(pairs==0):
                print("(",end="")
	    #s = ""
	    for j in i:
		print(j,end="")
		s+=j
	    if(pairs==0):
		print(",",end="")
		if(self.is_float(s) or self.is_int(s)):
		    self.AddLists(L1,s)        

		pairs+=1
	    elif(pairs==1):
	        print(")",end="")
		if(self.is_float(s) or self.is_int(s)):
		    self.AddLists(L1,s)
		EE.append(L1)
		L1 = []		
		pairs=0
	    if Lines==2:
	        print("",end = "\n")
		EE.append(['---'])
	print("[-Env-],",EE,'[-Start+Goal Pairs-]',end="\n")
