import sys
import afl 
import os

#-----------------------------------------
#   Place test function here
#-----------------------------------------

def testFunction(a,b,c):
    x,y,z = 0, 0, 0
    if (a):
        x = -2
    if (b < 5):
        if (not a and c):
            y = 1
        z = 2
    assert(x + y + z != 3)            

def main():
    in_str = sys.stdin.read()
    a, b, c = in_str.strip().split(" ")
    a = int(a)
    b = int(b)
    c = int(c)

    testFunction(a,b,c)

if __name__ == "__main__": 
    afl.init()       
    main()
    os._exit(0)
    
