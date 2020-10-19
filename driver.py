import sys
import os
import numpy


if __name__ == "__main__":
    test = sys.argv[1]
    k = sys.argv[2]
    ##for x in range(10,int(k)+1):
    for x in range(5):
        os.system("python KNN.py 10 "+test+" "+str(k))
    for x in range(5):
        os.system("python KNN.py 20 "+test+" "+str(k))
    for x in range(5):
        os.system("python KNN.py 30 "+test+" "+str(k))
    for x in range(5):
        os.system("python KNN.py 40 "+test+" "+str(k))
    for x in range(5):
        os.system("python KNN.py 50 "+test+" "+str(k))
    for x in range(5):
        os.system("python KNN.py 60 "+test+" "+str(k))
    for x in range(5):
        os.system("python KNN.py 70 "+test+" "+str(k))
    for x in range(5):
        os.system("python KNN.py 80 "+test+" "+str(k))
    for x in range(5):
        os.system("python KNN.py 90 "+test+" "+str(k))
    for x in range(5):
        os.system("python KNN.py 100 "+test+" "+str(k))

    