import sys
import os
import numpy
import statistics 


if __name__ == "__main__":
    file = sys.argv[1]
    data = sys.argv[2]
    f = open(file,"r+")
    fs = open(file[:-4]+"calcs.txt","w+")
    dataa = [0,0,0,0,0]
    vdata = [0,0,0,0,0]
    x = 0
    for k in range(50):
        ##print(x)
        entry = next(f)[:-1]
        dataa[x] = float(entry)
        if(data == "2"):
            entry = next(f)
            vdata[x] = float(entry[:-1])
        if(x == 4):
            ##print(data)
            fs.write("Percentage: "+str(100*((k+1)/50))+"%\n")
            fs.write("Testing: \n")
            answer = 100*statistics.stdev(dataa)
            fs.write("Stdev: "+str(answer)+"%\n")
            answer = 100*statistics.mean(dataa)
            fs.write("Mean: "+str(answer)+"%\n")
            if(data == "2"):
                fs.write("Validating: \n")
                answer = 100*statistics.stdev(vdata)
                fs.write("Stdev: "+str(answer)+"%\n")
                answer = 100*statistics.mean(vdata)
                fs.write("Mean: "+str(answer)+"%\n")
            x = 0
            fs.write("\n")
        else:
            x = x+1
    