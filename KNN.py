import sys
import os
import numpy
import random
import time

if __name__ == "__main__":
    
    print("Running KNN")
    percent = float(sys.argv[1])
    mode = sys.argv[2]
    dimx = 0
    dimy = 0
    train,trainl,test,testl,validation,validationl = ["" for _ in range(6)]
    curr = os.getcwd()
    if(mode == "digit"):
        dimx = 28
        dimy = 28
        train = curr+"/data/digitdata/trainingimages"
        trainl = curr+"/data/digitdata/traininglabels"
        test =  curr+"/data/digitdata/testimages"
        testl = curr+"/data/digitdata/testlabels"
        testv = curr+"/data/digitdata/validationimages"
        testvl = curr+"/data/digitdata/validationlabels"
    elif(mode == "face"):
        dimx = 60
        dimy = 70
        train = curr+"/data/facedata/facedatatrain"
        trainl = curr+"/data/facedata/facedatatrainlabels"
        test =  curr+"/data/facedata/facedatatest"
        testl = curr+"/data/facedata/facedatatestlabels"
        testv = curr+"/data/facedata/facedatavalidation"
        testvl = curr+"/data/facedata/facedatavalidationlabels"
        
    else:
        print("Invalid Mode")
        exit()
        
    answersu = []
    answers = []
    testsize = 0
    select = 0
    data = []
    flat = []
    start = time.time()
    if(os.path.exists(train) and os.path.exists(trainl)):
        print("Extracting Training Data")
        ##extract labels and get size of data set
        fl = open(trainl,"r+")
        for entry in fl:
            value = entry[0:-1]
            answers.append(int(value))
        fl.close()
        data = numpy.zeros((len(answers),dimx,dimy),int)
        f = open(train,"r+")
        ##extract images
        testsize = int(len(answers)*(percent/100))
        for k in range(0,len(answers)):
            for y in range(0,dimy):
                line = next(f)
                for x in range(0,dimx):
                    if(ord(line[x]) == 32):
                        data[k][x][y] = 0
                    elif(ord(line[x]) == 35):
                        data[k][x][y] = 1
                    elif(ord(line[x]) == 43):
                        data[k][x][y] = 2
            flat.append(data[k].flatten('F'))
        f.close()
        ##remove random entries until testsize is correct
        while(len(flat)>testsize):
            slot = int(random.random()*len(flat))
            answers.pop(slot)
            flat.pop(slot)
    else:
        print("Files are Missing")
    print("Training Set Size: "+str(len(flat)))
    end = time.time()
    f = open("KNNtimes.txt","a+")
    f.write(str(end - start)+"\n")
    answerst = []
    answersv = []
    testsizet = 0
    datat = []
    datav = []
    flatt = []
    flatv = []
    if(os.path.exists(test)and os.path.exists(testl)):
        print("Extracting Testing Data")
        fl = open(testl,"r+")
        ##extract labels and get size of data set
        for entry in fl:
            value = entry[0:-1]
            answerst.append(int(value))
        fl.close()
        datat = numpy.zeros((len(answerst),dimx,dimy),int)
        f = open(test,"r+")
        ##extract images
        for k in range(0,len(answerst)):
            for y in range(0,dimy):
                line = next(f)
                for x in range(0,dimx):
                    if(ord(line[x]) == 32):
                        datat[k][x][y] = 0
                    elif(ord(line[x]) == 35):
                        datat[k][x][y] = 1
                    elif(ord(line[x]) == 43):
                        datat[k][x][y] = 2
                    else:
                        datat[k][x][y] = ord(line[x])
            flatt.append(datat[k].flatten('F'))
        f.close()
    else:
        print("Files are Missing")
    print("Test Set Size: "+str(len(flatt)))
    if(os.path.exists(testv)and os.path.exists(testvl)):
        print("Extracting Validation Data")
        fl = open(testvl,"r+")
        for entry in fl:
            value = entry[0:-1]
            answersv.append(int(value))
        fl.close()
        datav = numpy.zeros((len(answersv),dimx,dimy),int)
        f = open(testv,"r+")
        for k in range(0,len(answersv)):
            for y in range(0,dimy):
                line = next(f)
                for x in range(0,dimx):
                    if(ord(line[x]) == 32):
                        datav[k][x][y] = 0
                    elif(ord(line[x]) == 35):
                        datav[k][x][y] = 1
                    elif(ord(line[x]) == 43):
                        datav[k][x][y] = 2
                    else:
                        datav[k][x][y] = ord(line[x])
            flatv.append(datav[k].flatten('F'))
        f.close()
    else:
        print("Files are Missing")
    print("Validation Set Size: "+str(len(flatt)))
    print("Extraction Complete")
    f = open("results.txt","w+")
    k = int(sys.argv[3])
    if(k>0):
        print("Testing:")
        testnum = 0
        correct = 0
        for testv in flatt:
            if(mode == "digit"):
                if(testnum % 100 == 0):
                    print(str(testnum)+"/"+str(len(answerst))+" Done")
            elif(mode == "face"):
                if(testnum % 50 == 0):
                    print(str(testnum)+"/"+str(len(answerst))+" Done")
            distlist = numpy.zeros((1,2),float)
            distlist = distlist.tolist()
            trainnum = 0
            for trainv in flat:
                dist = numpy.linalg.norm(trainv-testv)
                if(trainnum == 0):
                    distlist[0][0] = dist
                    distlist[0][1] = answers[trainnum]
                else:
                    add = 0
                    slot = 0
                    if(dist<distlist[len(distlist)-1][0]):
                        for entry in distlist:
                            if(entry[0]>dist):
                                distlist.insert(slot,(dist,answers[trainnum]))
                                if(len(distlist)>k):
                                    distlist.pop()
                                add = 1
                                break
                            slot = slot + 1
                            if(slot>=k):
                                break
                        if(add == 0 and len(distlist)<k):
                            distlist.append((dist,answers[trainnum]))
                trainnum = trainnum+1
            modes = []
            if(sys.argv[2] == "digit"):
                modes = [0,0,0,0,0,0,0,0,0,0]
            if(sys.argv[2] == "face"):
                modes = [0,0]
            for entry in distlist:
                #f.write(str(entry)+"\n")
                modes[entry[1]] = modes[entry[1]] + 1
            min = 0;
            for x in range(len(modes)):
                if(modes[min]<=modes[x]):
                    if(modes[min]==modes[x]):
                        for entry in distlist:
                            if(entry[1] == x):
                                min = x
                                break
                            if(entry[1] == min):
                                break
                    else:
                        min = x
            if(min == answerst[testnum]):
                correct = correct + 1
                f.write(str(min)+" "+str(answerst[testnum])+" Correct\n")
            else:
                f.write(str(min)+" "+str(answerst[testnum])+" \n")
            testnum = testnum +1
        print(str(correct)+"/"+str(len(answersv))+" Correct")
        print(100*correct/len(answerst))
        fa = open("testing.txt","a+")
        fa.write(str(100*correct/len(answerst))+"\n")


        testnum = 0
        correct = 0
        print("Validating:")
        for testv in flatv:
            if(mode == "digit"):
                if(testnum % 100 == 0):
                    print(str(testnum)+"/"+str(len(answersv))+" Done")
            elif(mode == "face"):
                if(testnum % 50 == 0):
                    print(str(testnum)+"/"+str(len(answersv))+" Done")
            distlist = numpy.zeros((1,2),float)
            distlist = distlist.tolist()
            trainnum = 0
            for trainv in flat:
                dist = numpy.linalg.norm(trainv-testv)
                if(trainnum == 0):
                    distlist[0][0] = dist
                    distlist[0][1] = answers[trainnum]
                else:
                    add = 0
                    slot = 0
                    if(dist<distlist[len(distlist)-1][0]):
                        for entry in distlist:
                            if(entry[0]>dist):
                                distlist.insert(slot,(dist,answers[trainnum]))
                                if(len(distlist)>k):
                                    distlist.pop()
                                add = 1
                                break
                            slot = slot + 1
                            if(slot>=k):
                                break
                        if(add == 0 and len(distlist)<k):
                            distlist.append((dist,answers[trainnum]))
                trainnum = trainnum+1
            modes = []
            if(sys.argv[2] == "digit"):
                modes = [0,0,0,0,0,0,0,0,0,0]
            if(sys.argv[2] == "face"):
                modes = [0,0]
            for entry in distlist:
                #f.write(str(entry)+"\n")
                modes[entry[1]] = modes[entry[1]] + 1
            min = 0;
            for x in range(len(modes)):
                if(modes[min]<=modes[x]):
                    if(modes[min]==modes[x]):
                        for entry in distlist:
                            if(entry[1] == x):
                                min = x
                                break
                            if(entry[1] == min):
                                break
                    else:
                        min = x
            if(min == answersv[testnum]):
                correct = correct + 1
                f.write(str(min)+" "+str(answersv[testnum])+" Correct\n")
            else:
                f.write(str(min)+" "+str(answersv[testnum])+" \n")
            testnum = testnum +1
        print(str(correct)+"/"+str(len(answersv))+" Correct")
        print(100*correct/len(answersv))
        fa = open("testing.txt","a+")
        fa.write(str(100*correct/len(answersv))+"\n")
        fa.close()
        f.close()    
        
    exit()