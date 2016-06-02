""" This is meant to demonstrate how easy it is to throw the functions from phist into a framework """

from sys import argv
from phist import *


class phistAction:
    def __init__(self, *args):
        self.hashDirectory = 0
        self.hashImage = 0
        self.directoryCheck = 0
        self.imageCheck = 0
        self.delete = 0
        
        # Should be using argParse
        
        
        if argv[1] == "-dh":
            self.hashDirectory = 1
            self.dirToHash = argv[2]
            self.flatDbName = argv[3]
        elif argv[1] == "-ih":
            self.hashImage = 1
            self.imgToHash = argv[2]
            self.flatDbName = argv[3]
        elif argv[1] == "-dc":
            self.directoryCheck = 1
            self.queryDirectory = argv[2]
            self.flatDbName = argv[3]
        elif argv[1] == "-ic":
            self.imageCheck = 1
            self.imageName = argv[2]
            self.flatDbName = argv[3]
        elif argv[1] == "-delete":
            self.delete = 1
            self.flatDbName = argv[2]

        if self.hashDirectory == 1:
            self.hDirectory()
        elif self.hashImage == 1:
            self.hImage()
        elif self.directoryCheck == 1:
            self.cDirectory()
        elif self.imageCheck == 1:
            self.cImage()
        elif self.delete == 1:
            delete(self.flatDbName)
        else:
            print("Command line options are:\n\t <-dh(hash directory), -ih(hash image), -dc(check directory), -ic(check image)> queriedPath flatFile\nOr to delete:\n\t -delete flatFile")


    def hDirectory(self):
        hashDirectory(self.dirToHash, self.flatDbName)
        
    def hImage(self):
        hashImage(self.imgToHash, self.flatDbName)

    def cImage(self):
        returned = imageChecker(self.imageName)
        print(returned)

    def cDirectory(self):
        returned = directoryChecker(self.queryDirectory)
        
        print("\n\tFile Queried:\t\tFile Matched:\t\tDate Entered:\n")
        for i in returned:
           
            s = "\t" + str(i[0].split("/")[-1]) + ":"
            
          
            while len(s) < 20:
                s += " "
                
            s += "\t"  + i[1][2][0][0] + "\t""\t" + i[1][2][0][1] 
            print(s)      
        print("\n") 
    


a = phistAction()
