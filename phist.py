###################################################################
#
#		p.h.i.s.t.
#
#	    Perceptual Hashing Image Similarity Tool 
#
#                             As Written By MIDN Dennis Devey
#                                                 29 Mar 2016
#
###################################################################

""" This tool is written to be run with Python 3.x in Ubuntu 14.04 """
""" Ensure that all dependencies are filled """

""" sudo apt-get install update upgrade python-pip libjpeg-dev zlib1g-dev python-dev python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose """
""" pip install Pillow """

#General Dependencies
from os import getcwd
from os import listdir
from os import rename
from os import system
from os.path import join

import itertools
from collections import defaultdict
import time
import pickle

#Image Hashing Dependencies
from PIL import Image
import numpy
import scipy.fftpack
import numpy as np

####################################
#
#  Highest Level Functions
#
#
####################################

""" These are the functions that you will call from your existing frameworks """
""" Each is very simple, and calls a pile of other functions, but all that your tool needs to know about are these four """

""" Hash a single image and add it to your database """
def hashImage(image, flatDbName):
    writeHash(image, flatDbName)

""" Hash a directory of images and add it to your database """
def hashDirectory(dirToHash, flatDbName):
    newFile(dirToHash, flatDbName)

""" Check a single image against your database """
def imageChecker(image):
    databaseLoad() # load database from .pickle files
    return checkImage(image) # return information about matching image in the form of a list of lists, if no match, return false
    
""" Check a directory of images against your database """
def directoryChecker(queryDirectory):
    databaseLoad() # load database from .pickle files
    
    listOfImages = directoryEater(queryDirectory) # Get a list of images from the specified directory

    returned = [] # Create empty list to return eventually
    for image in listOfImages: # Iterate through images

        tmp = checkImage(image) # Check each image against database

        if tmp: # If check returns true it is a match
            returned.append([image, tmp]) # Append the data to a lsit
    return returned # Return list of lists
    
def delete(flatDbName):
    system("rm " + flatDbName)
    system("rm averageHash64.pickle")
    system("rm averageHashBuckets.pickle")
    print(flatDbName + " Deleted")
####################################
#
#  Image Data Functions
#        [ ] Pull out metadata and include in returned data
#        [ ] Add whatever else you want to provide context for images
#
####################################
""" 
This section does not contain much at this point 
Should eventually contain all functions related to providing context to an image in the database 
"""

def getData(image):
    """ Currently returns image name and date indexed"""
    """ Can easily be expanded to get any sort of image specific data """
    
    dateAdded = time.strftime("%H:%M %d/%m/%Y").strip() # gets time and date

    return image, dateAdded  

####################################
#
#  Database Query
#        [ ] Migrate to a relational database
#        [ ] Implement a k-d tree in each bucket 
#
####################################
""" 
The current implementation is an amalgamation of flat files, .pickles, and memory
This is a proof of concept
I highly recommend transitioning to whatever relational database you feel comfortable implementing a k-d tree in 
"""

def checkHashes(imgHashes): 
    """ Queries an images hashes against the database """
    """ Returns data if match, returns false if no match is found """

    """ The first check IS NOT NECESSARY, however, I like to have it because it lets me know when I have an exact match. """
    """ If you wish to save some storage space, comment out any references to a25 throughout this script """
    if imgHashes[0][0] in a25:  # Check average hashtable for exact match of hash
        return "a25", imgHashes[0][0], a25[imgHashes[0][0]]
     
        """ If you get rid of all references to a25, this will be the top line in checkHashes() """
        """ You will not have any new false negatives, and the storage space will be about 1/3 less """
    elif imgHashes[0][1] in aBuckets:  # If 6 byte hash in aBuckets
        bucket = aBuckets[imgHashes[0][1]]
        for i in bucket:  # Should be a k-d tree. 
            """ As a k-d tree, this will provide log(n) time lookups in each bucket """
            """ I have made no attempt to optimize this implementation"""
            
            h1 = hamming1(imgHashes[0][2], i[0]) # Get hamming distance between queried image and item in bucket
 
            if h1 < 3: # Three is a totally arbitrary number, tune as you would like

                return("aBk", i[0], a25[i[1]])
            else:  # Image not in database
                return False
    else:  # Does not match any buckets
        return False
        
def hamming1(str1, str2):  
    """ Used in buckets """
    """ Returns hamming distance between two strings """
    """ I know that the strings _SHOULD_ be a byte array, but the speed 
    increase would be inconsequential for the amount of effort required"""
    
    return sum(itertools.imap(str.__ne__, str1, str2))

####################################
#
#  Database Creation
#        [x] Pickel variables in memory for speedy loads
#        [ ] Migrate to a relational database
#
####################################
"""
These are all the functions required to create the database.

This version uses a dictionary of 25 byte hashes and a hashtable of 6 byte hashes that contain buckets filled with 25 byte hashes.

When hashing an image or directory, the new hash(es) are appended to a flat file, and then two new pickles are created. 
If you do not know what pythonic pickling is, documentation can be found here: https://docs.python.org/3/library/pickle.html

With pickling, we are able to query the database without having to load the flat file into memory every single time,
allowing for sigficantly better performance.
"""

def databaseBuilder(hashList):  

    global a25 # Declaring them as globals
    global aBuckets
    a25 = defaultdict(list)  # 25 byte average hash table
    aBuckets = defaultdict(list)  # Staggered(6 byte -> 25 byte) average hash table

    """ Given a list of hashes, creates required database """

    for i in hashList:

        a25[i[0][0]].append(list(i[1]))
        aBuckets[i[0][1]].append((i[0][2], i[0][0]))
        
    """ I recommend reading the documentation for pickling if you are unfamiliar with pickling """
    """ https://docs.python.org/3/library/pickle.html """
    """ The general idea is that we are saving the data structures from memory so that we 
    are able to load them instantly next time the program is run, rather than loading from a flat file """
    
    with open('averageHash64.pickle', 'wb') as f: # Names are hard coded in, probably shouldn't be
        pickle.dump(a25, f, pickle.HIGHEST_PROTOCOL)
    with open('averageHashBuckets.pickle', 'wb') as f:
        pickle.dump(aBuckets, f, pickle.HIGHEST_PROTOCOL)
        
def databaseLoad():  
    """ Loads pickled files from local directory into global variables """
    """ VERY FAST in comparison to loading large flat file every time, allows more queries per second """
    
    
    global a25 # Declaring as globals
    global aBuckets
    a25 = defaultdict(list)  # 25 byte average hash table
    aBuckets = defaultdict(list)  # Staggered(6 byte -> 25 byte) average hash table

    with open('averageHash64.pickle', 'rb') as f: # Names should not be hard coded
        a25 = pickle.load(f)
        f.close()
    with open('averageHashBuckets.pickle', 'rb') as g:
        aBuckets = pickle.load(g) 
        g.close()
        

def writeHashes(hashes, flatFileName):  
    """ Writes an image's hashes to a flat file """

    f = open(flatFileName, 'a')  # Open flatFile to append to

    f.write('%s, %s, %s, %s, %s\n' % (hashes[0][0], hashes[0][1], hashes[0][2], hashes[1][0], hashes[1][1]))
    f.close()  # File close
    return hashes[0], hashes[1]


def newFile(directoryName, flatFileName):  
    """ Create a new flatFile from a directory of images """
    
    listOfFiles = directoryEater(directoryName)
    bulkFlatFileWrite(listOfFiles, flatFileName)

def bulkFlatFileWrite(listOfFiles, dbName):  
    """ Given a list of files, write their full hashes to specified flat file """
    
    listOfHashes = []
    for i in listOfFiles:
        listOfHashes.append(getHashes(i))
    writeMassHashes(listOfHashes, dbName)

def writeMassHashes(listOfHashes, flatFileName):  
    """ Writes a list of hashes to a flat file """
    
    listToWrite = []
    for hashes in listOfHashes:
        listToWrite.append('%s, %s, %s, %s, %s\n' % (hashes[0][0], hashes[0][1], hashes[0][2], hashes[1][0], hashes[1][1]))

    f = open(flatFileName, 'a')  # Open flatFile to append to
    f.writelines(listToWrite)
    f.close()  # File close
    flatFileLoad(flatFileName)
    
def writeHash(fileName, flatFileName):  
    """ Writes a list of hashes to a flat file """
    hashes = getHashes(fileName)
    listToWrite = []
    listToWrite.append('%s, %s, %s, %s, %s\n' % (hashes[0][0], hashes[0][1], hashes[0][2], hashes[1][0], hashes[1][1]))
    f = open(flatFileName, 'a')  # Open flatFile to append to
    f.writelines(listToWrite)
    f.close()  # File close
    flatFileLoad(flatFileName)
    
def readHashes(flatFileName):  
    """ Reads hashes out of a flat file and returns a list of hashes for entry into databaseBuilder """
    
    with open(flatFileName, 'r') as f:
        hashes = f.readlines()
        fileHashes = []

        for line in hashes:
            c = line
            a = c.split(", ")
            fileHashes.append([(a[0], a[1], a[2]), (a[3], a[4].strip())])
        return fileHashes

def flatFileLoad(flatFileName): 
    """ Given the name of a flat file, loads all hashes into database """
    databaseBuilder(readHashes(flatFileName))     

   
####################################
#
#  Hashing Helper Functions
#
####################################
    
def directoryEater(directoryName):  
    """ Given a directory name, returns list of files in directory for entering into bulkLoader """
    
    path = getcwd()
    flatFileNamesWSpaces = listdir(path)
    for flatFileName in flatFileNamesWSpaces:
        rename(join(path, flatFileName), join(path, flatFileName.replace(" ", "-")))
    flatFileNames = listdir(directoryName)
    b = []
    for i in flatFileNames:
        b.append(directoryName + "/" + i)
    return b


def bulkLoader(listOfFiles): 
    """ Takes in a list of files and returns a list of their full hashes """
    
    hashList = []
    for flatFileName in listOfFiles:
        hashList.append(getHashes(flatFileName))
    return hashList
    
####################################
#
#  Higher Level Functions
#
####################################

def getHashes(image):
    """ Returns average hashes of an image, as well as any data """
    #print(ahashes(image))
    return [ahashes(image), getData(image)]
    
def ahashes(image):  
    """ Returns 64 byte, 4 byte, and 16 byte average hash"""
    
    return average_hash(Image.open(image))

def checkImage(image):
    """ Check an image against database """
    
    return checkHashes(getHashes(image))
    
####################################
#
#  Miscellany
#
####################################

"""
There's nothing in here, for now.
Function bloat will return.
"""

####################################
#
#	Image Hashing   
#    	                
####################################

"""
These are the requisite functions for turning images into hexadecimal strings.
My implementation was based off of Johannes Buchner's ImageHash, located at https://github.com/JohannesBuchner/imagehash
His implementation was forked off of PhotoHash, https://github.com/bunchesofdonald/photohash

My average hash function differs greatly from it's predecessors, everything else is essentially the same.

The length of the hashes returned is entirely arbitrary. Change them as you like, though you have to make sure that the numpy.reshape will still work.

"""

def average_hash(image, hash_size=10):
    """
    Average Hash Computation Implementation follows http://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html

    """
    
    image = image.convert("L").resize((hash_size, hash_size), Image.ANTIALIAS)
    # Grey scale and shrink the image to thumbnail size
    pixels = numpy.array(image.getdata()).reshape((hash_size, hash_size))
    # Convert the image to pixels
    avg = pixels.mean()
    # Get the avg color for all pictures
    origArray = pixels > avg
    # Compare the color of each pixel to the avg color for the picture and assign a one or zero accordingly

    sizeBig = 10 # Arbitrary size
    # Size of original hash (vaguely... 10 => 25)
    sizeSmall = 5 # Arbitrary size
    # Size of hash to be created (vaguely... 5 => 6)

    newArray = origArray.reshape([sizeSmall, sizeBig/sizeSmall, sizeSmall, sizeBig/sizeSmall]).mean(3).mean(1)
    # This part is pfm. We take the first matrix and resize it so that it is now a lower resolution version of the original
    
    newArray = np.around(newArray)
    # We round the averages so that we have nothing but 1's and 0's
    
    return toHashes(origArray, newArray, origArray) # Yes, it is a redundant hash. I haven't gotten around to removing it.
    # And then we convert the matrices into hashes


def toHashes(binary_array, binary_array2, binary_array3):
    """ Transmogrifies three arrays into three hexadecimal strings """
    hash1 = binary_array
    hash2 = binary_array2
    hash3 = binary_array3
    a = (_binary_array_to_hex(hash1.flatten()), _binary_array_to_hex(hash2.flatten()), _binary_array_to_hex(hash3.flatten()))
    return a


def _binary_array_to_hex(arr):
    """ Function to make a hex string out of a binary array """
    h = 0
    s = []
    for i, v in enumerate(arr.flatten()):
        if v:
            h += 2 ** (i % 8)
        if (i % 8) == 7:
            s.append(hex(h)[2:].rjust(2, '0'))
            h = 0
    return "".join(s)


"""
       ___________         
       |   ______  \               
       |  |      \  \                       
       |  |     __\__\____                        
       |  |   |   ______  \                 
       |  |   |  ||  |  \  \               
       |  |   |  ||  |   \  \               
       |  |   |  ||  |   |  |              
       |  |   |  |/  /   |  |                  
       |  |   |  /  /    |  |                       
       |  |___|_/  /     |  |                         
       |_________ /      /  /           
              |  |      /  /            
              |  |_____/  /                          
              |__________/   
                            
                             Contact me at d.m.devey@gmail.com 
              
"""
