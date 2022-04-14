import sys
import os

filePath=os.path.abspath('../Phase1/lex.py')
directory=os.path.dirname(filePath)
sys.path.append(os.path.split(directory)[0])
from Phase1 import lex

tableSize=20
#Note: that hashTable=[[]]*tableSize would not work because it would generate multiple copies of the same element;
#altering one element changes all of the other elements as well.
hashTable=[[] for i in range(tableSize)]

def insertToHashTable(string:str):
    hashNum=hash(string)
    index=hashNum % tableSize
    print(f"\tString:{repr(string)}, Hash:{hashNum}, HashIndex:{index}")
    hashTable[index].append(string)

def printHashTable():
    for i in range(len(hashTable)):
        print(f"Row {i} Length:{len(hashTable[i])}")
        print(f"\t{hashTable[i]}")

if __name__=='__main__':
    token=lex.getNextToken()
    while token:
        #token.printTokenInfo()
        insertToHashTable(token.getTokenStr())
        token=lex.getNextToken()
    print("--------- Hash Table ---------")
    printHashTable()

    print("--------- Transpose 2D array Method1---------")
    transposed=[]
    matrix=[[1,2,3,4],[4,5,6,8]]
    for i in range(len(matrix[0])):
        transposed_row=[]
        for row in matrix:
            transposed_row.append(row[i])
        transposed.append(transposed_row)
    print(transposed)

    print("--------- Transpose 2D array Method2---------")
    transpose=[[row[i] for row in matrix] for i in range(len(matrix[0]))]
    print(transpose)
