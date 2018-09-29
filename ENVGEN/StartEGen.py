from EnvGen import EnvGen
from MapMake import mapMake

import sys

def main():
    if(len(sys.argv[:])<2):
        print("MUST ENTER MAP PATH IN ARG 1")
	sys.exit(-1)
    print("Start")
    E = EnvGen()
    M = E.CreateENV(sys.argv[1])

    mapMake(M)
if __name__=="__main__":
    main()
