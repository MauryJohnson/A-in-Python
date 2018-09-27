from EnvGen import EnvGen

import sys


def main():
    if(len(sys.argv[:])<2):
        print("MUST ENTER MAP PATH IN ARG 1")
	sys.exit(-1)
    print("Start")
    E = EnvGen()
    E.CreateENV(sys.argv[1])
if __name__=="__main__":
    main()
