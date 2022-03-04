"""
Name: Kenniel Torres

-Notes-
> Requires MurmurHash3 Library. For more information: https://pypi.org/project/mmh3/
> To install, run the following command line: pip install mmh3
> Tested with Python 3.8
"""

import csv
import math
import mmh3

def main():
        #Input file from which we'll create the Bloom Filter
        fileInput = str(input("Which file do you want?\nDo not include extension! ")) + ".csv"
        print(" ")
        #Input file to which we will compare the hashing
        fileInput2 = str(input("Which file do you want for comparison?\nDo not include extension! ")) + ".csv"
        print(" ")
        with open(fileInput) as fileToRead, open(fileInput) as fileSize, open(fileInput2, 'r') as compareFile:
            fileLength = len(list(fileSize)) #Number of rows in csv file 1
            bloomFilter1 = BloomFilter(0.0000001) #Creates a Bloom Filter instance
            reader = csv.reader(fileToRead) #Reader for fileToRead
            comparisonReader = csv.reader(compareFile) #Comparison reader for compareFile
            createOutput(bloomFilter1.createHashList(bloomFilter1.hashCount(bloomFilter1.createBFSize(fileLength), fileLength), fileLength, reader, comparisonReader))


"""
Parameter:
emailList = Results list containing emails and their values
"""
def createOutput(emailList): #Creates csv file, in the same directory as .py file, containing results from the Bloom Filter
    with open("Results.csv",'w', newline = '') as newfile:
        newFileWriter = csv.writer(newfile)
        newFileWriter.writerows(([row] for row in emailList))
        newfile.close()

"""
Parameter:
falsePositive = False Positivity Rate in decimal form (ej: BloomFilter(0.1))
"""
class BloomFilter: #Bloom Filter

    def __init__(self, falsePositive):
        self.falsePositive = falsePositive

    def createBFSize(self, n): #(m) Calculates Bloom Filter Size (bits)
        bFSize = math.ceil(n * math.log(self.falsePositive, math.e) / math.log(1/math.pow(2, math.log(2, math.e)), math.e))
        return bFSize

    def hashCount(self, m, size): #(k) Calculates Hash Count (number of functions needed)
        hashCount = round((m / size) * math.log(2, math.e))
        return hashCount

    #Creates Hash List for Bloom Filter instance
    def createHashList(self, k, size, fileReader, compareReader):
        hashList = []
        resultList = []
        bloomFilterSize = round(self.createBFSize(size))
        #Creates empty list used for hashing
        for i in range(bloomFilterSize):
            hashList.append(0)

        #Iterates each email, 'k' times, and inserts '1' at calculated hash values
        for row in fileReader:
            for n in range(k):
              hashList[mmh3.hash(row[0], n) % bloomFilterSize] = 1

        #Compares values of second file to verify if it is 'possibly stored' or not
        for line in compareReader:
            notInHash = False
            if line[0] == "Email":
                resultList.append(line[0] + ", Results")
                continue
            for n in range(k):
                if hashList[mmh3.hash(line[0], n) % bloomFilterSize] == 0:
                    notInHash = True
                    break
            if(notInHash):
                resultList.append(line[0] + ", Not in the DB")
                notInHash = False
            elif(not notInHash):
                resultList.append(line[0] + ", Probably in the DB")

        print("Hash Count: ", k)
        print("Bloom Filter Size: ", bloomFilterSize)
        return resultList

if __name__ == "__main__":
    main()
