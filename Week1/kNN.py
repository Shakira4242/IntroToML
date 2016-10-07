"""

kNN: k Nearest Neighbors

"""
from numpy import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import operator
from PIL import Image
from os import listdir
from sklearn.neighbors import KNeighborsClassifier

def classify0(inX, dataSet, labels, k):

    ''' 
        =============
        training data 
        ============= 

        consists of:

        1. attributes
    
            ex:[[0,0,0,0,0,0,0,0,0], 
                [0,0,0,1,1,1,0,0,0],
                [0,0,1,1,1,1,1,0,0],
                [0,1,1,0,0,0,1,1,0],
                [0,1,1,0,0,0,1,1,0],
                [0,1,1,0,0,0,1,1,0],
                [0,1,1,0,0,0,1,1,0],
                [0,0,1,1,1,1,1,0,0],
                [0,0,0,1,1,1,0,0,0],
                [0,0,0,0,0,0,0,0,0]]

                or 


               [[0,0,0,0,0,0,0,0,0],
                [0,0,0,0,1,0,0,0,0],
                [0,0,0,1,1,0,0,0,0],
                [0,0,0,0,1,0,0,0,0],
                [0,0,0,0,1,0,0,0,0],
                [0,0,0,0,1,0,0,0,0],
                [0,0,0,0,1,0,0,0,0],
                [0,0,0,0,1,0,0,0,0],
                [0,0,1,1,1,1,1,0,0],
                [0,0,0,0,0,0,0,0,0]]


                or


                [[0,0,0,0,0,0,0,0,0],
                [0,0,0,0,1,0,0,0,0],
                [0,0,0,1,1,1,0,0,0],
                [0,0,1,0,0,1,1,0,0],
                [0,0,0,0,0,1,1,0,0],
                [0,0,0,0,0,1,1,0,0],
                [0,0,0,0,0,1,1,0,0],
                [0,0,0,0,1,1,0,0,0],
                [0,0,1,1,1,1,1,1,0],
                [0,0,0,0,0,0,0,0,0]]

        2. labels
        
            ex: [0,1,2,3,4,5,6,7,8,9]


        =============
        test data
        =============

        1. Attributes without lables

        Note: The test data doesn't have labels. Our goal is to classify this test data (matrices) with the best accuracy.
    
    '''

    
    # In our example dataSet is the training data while inX is the test
    
    # Get the number of columns in the training dataset
    dataSetSize = dataSet.shape[0]

    # Get the Euclidean distance between test vector and training data
    diffMat = tile(inX, (dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5

    # sort the distances
    sortedDistIndicies = distances.argsort()   

    # Make a dictionary called classCount which will keep the names of the labels with the least distance
    classCount={}  

    # this loop might be a bit confusing
    # Here's some pseudocode:
    #   Loop over k times
    #       get the label with the least distance
    #       now add 1 to the classCount
    #   
    #   Sort the classCount in ascending Order
    #   Return the highest classCount

    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    print(sortedClassCount)
    return sortedClassCount[0][0]
    
def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect

def handwritingNumberDetector():

    # let's put all the labels aka [0,1,2,3,4,5,6,7,8,9] in this array
    hwLabels = []

    # let's put all the attributes aka matrices of 0's and 1's into an array
    trainingMat = []

    # link to the directory with all our training data
    trainingFileList = listdir('digits/trainingDigits')
    trainingFileList.pop(0)
    m = len(trainingFileList)


    # we know how long our trainingMat is so let's initialize it with zeros
    trainingMat = zeros((m,1024))

    # In this loop we do 2 things:
        # get labels and add them to hwLabels
        # get attributes and add them to trainingMat

    for i in range(0,m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = fileStr.split('_')[0]
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2vector('digits/trainingDigits/%s' % fileNameStr)

    # Recap:
        # trainingMat has training data attributes
        # hwLabels has training data labels

    # link to the directory with all our test data
    testFileList = listdir('digits/testDigits') 

    # don't worry about these for now
    errorCount = 0.0
    mTest = len(testFileList)

    # In this loop we:
        # get attributes from the test data
        # Use the attributes as an argument to our kNN algorithm

    # for i in range(1,mTest):
    #     fileNameStr = testFileList[i]
    #     fileStr = fileNameStr.split('.')[0]
    #     classNumStr = fileStr.split('_')[0]
    #     vectorUnderTest = img2vector('digits/testDigits/%s' % fileNameStr)
    #     #classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
    #     kNN = KNeighborsClassifier(n_neighbors = 3)
    #     kNN.fit(trainingMat,hwLabels)
    #     classifierResult = kNN.predict(vectorUnderTest)[0]
    #     print "the classifier came back with: %s, the real answer is: %s" % (classifierResult, classNumStr)
    #     if (classifierResult != classNumStr): errorCount += 1.0
    # print "\nthe total number of errors is: %d" % errorCount
    # print "\nthe total error rate is: %f" % (errorCount/float(mTest))




    img = Image.open('1.jpg')
    gray = img.convert('1')
    img = gray
    img.thumbnail((32,32), Image.ANTIALIAS)
    img.save('resizedImg.jpg')
    img = mpimg.imread('resizedImg.jpg')


    for i in range(len(img)):
        row = []
        for j in range(len(img[i])):
            if img[i][j] > 240:
                img[i][j] = 0
            else:
                img[i][j] = 1

    imgVector = img.flatten()
    print(img.shape)

    classifierResult = classify0(imgVector, trainingMat, hwLabels, 3)
    print(classifierResult)



