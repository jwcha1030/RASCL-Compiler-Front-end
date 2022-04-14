import re
import sys

def readAFile(filename:str):
    with open(filename,'r') as file:
        wholeFile=file.read()
        length=len(wholeFile)
        print(re.escape(wholeFile))
        findComments(wholeFile)
        countLines(wholeFile)

def findComments(string):

        pattern= '/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/|(//.*)'
        match=re.finditer(pattern, string)
        if match:
            print("Length:",len(re.findall(pattern,string)))
            for i in match:
                print(i)
        else:
            print("NO MATCH!")

def countLines(string):
    pattern = '.*[\r\n]'
    match = re.finditer(pattern, string, re.MULTILINE)
    if match:
        print("Length:", len(re.findall(pattern,string)))
        for line in match:
            print(line.group(0)[0:10])

def initLexer(source):
    with open(source,'r') as file:
        lineNum=1
        wholeFile=file.read()
        li=0 #whole file index
        x0=li #start index of a line
        xi=li #line index
        length= len(wholeFile)
        while li<length:
            print(f"Current Line.Index: {lineNum}.{xi}, Character {wholeFile[li]}")
            if re.match(r'[ \t]',wholeFile[li]):
                li+=1
                xi+=1
            else:
                nextLineMatch=re.match('[\n]',wholeFile[li])
                if nextLineMatch:
                    li+=1
                    lineLength=li-x0
                    line=wholeFile[x0:li]
                    print(f"LineNumber: {lineNum}, Length:{lineLength}, Line: {re.escape(line)}")
                    xi=0
                    x0=li
                    lineNum+=1
                else:
                    li+=1
                    xi+=1







if __name__ == '__main__':
    filename=sys.argv[1]
    #readAFile(filename)
    initLexer(filename)
