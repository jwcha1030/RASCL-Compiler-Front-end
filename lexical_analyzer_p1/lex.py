import sys
import re
tokens_relop={'=':'ASSIGN','<':'LT', '<=':'LE', '>':'GT', '>=':'GE', '==':'EQ', '!=':'NE',
        '!':'NOT', '&&':'AND', '||':'OR'}
tokens_op={'+':'PLUS', '-':'MINUS', '*':'MULT', '/':'DIV'}
tokens_punc={';':'SEMICOLON', '(':'LPAREN', ')':'RPAREN', ',':'COMMA', '{':'LBRACE','}':'RBRACE','[':'LBRACKET',
        ']':'RBRACKET'}
tokens_nonOp={'if':'IF', 'else':'ELSE', 'while':'WHILE','int':'INT', 'float':'FLOAT',
        'identifier':'ID', 'int_const':'ICONST', 'float_const':'FCONST', 'comment':'COMMENT',
        'print':'PRINT', 'read':'READ', 'function': 'FUNCTION'};
__listOfTokens=[]
tokenIndex=0

class Token():
    def __init__(self, tokenStr, tokenType, lineNum, lineIndex):
        #protected attributes (only by the naming convention)
        self._tokenStr=tokenStr #literal token string
        self._tokenType=tokenType #type of the token (e.g., ICONST)
        self._lineNum=lineNum # line number where the token exists
        self._lineIndex=lineIndex #starting index(inclusive) where the token starts in the line

    def printTokenInfo(self):
        if self._tokenType in list(tokens_op.values())+list(tokens_relop.values())+ list(tokens_punc.values()):
            print(f'{self._tokenType} [Line:Index]: [{self._lineNum}:{self._lineIndex}]')
        elif self._tokenType == 'ID':
            print(f'ID: {self._tokenStr} [Line:Index]: [{self._lineNum}:{self._lineIndex}]')
        elif self._tokenType =='ICONST' or self._tokenType == 'FCONST':
            print(f'{self._tokenType}: {self._tokenStr} [Line:Index]: [{self._lineNum}:{self._lineIndex}]')
        elif self._tokenType == 'COMMENT':
            print(f'{self._tokenType}:\n{self._tokenStr}\n[Line:Index]: [{self._lineNum}:{self._lineIndex}]')
        elif self._tokenType == 'NEXTLINE_DELIM':
            print(f'{self._tokenType} [Line:Index]: [{self._lineNum}:{self._lineIndex}]')
        else:
            print(f'Keyword: {self._tokenType} [Line:Index]: [{self._lineNum}:{self._lineIndex}]')

    def getTokenStr(self):
        return self._tokenStr

    def getTokenType(self):
        return self._tokenType

    def getTokenLine(self):
        return self._lineNum

    def getTokenLineIndex(self):
        return self._lineIndex

    def equals(self, token) -> bool:
        if self._tokenStr != token._tokenStr:
            return False
        if self._tokenType != token._tokenType:
            return False
        if self._lineNum != token._lineNum:
            return False
        if self._lineIndex != token._lineIndex:
            return False
        return True

def __initLexer(sourcefile):
    with open(sourcefile,'r') as file:
        lineNum=1
        #we are not investigating line by line (i.e., not using readlines()) because comments can be multilines
        #and investigating lexemes per line  will not allow us to find them.
        fileStr= file.read()
        #we need to track indices, one for the whole file and the others for each line to give more token info to the parser.
        li=0 #lexeme index scanning through the whole file string
        x0=li #the start index of a line (index relative to the whole file string)
        xi=li #the index within a line (refreshes to 0 every line unlike li)
        length= len(fileStr)
        while li<length:
            currChar=fileStr[li]
            #print(f"Current Line.Index: {lineNum}.{xi}, Character: {currChar}")
            #note that the below does not match the next line characters because we'll do so later.
            if re.match(r'[ \t]', currChar):
                li+=1
                xi+=1
            else:
                nextLineMatch=re.match('[\r\n]',currChar)
                if nextLineMatch:
                    #delimToken = Token(nextLineMatch.group(0), "NEXTLINE_DELIM",lineNum,xi)
                    #__listOfTokens.append(delimToken)
                    li+=1
                    lineLength=li-x0
                    lineStr=fileStr[x0:li]
                    #print(f'LineNumber: {lineNum}, Length: {lineLength}, LineStr: {re.escape(lineStr)}')
                    xi=0 #reset the tracking index of a line
                    x0=li #reset the starting index of a line
                    lineNum+=1
                else:
                    li0= li #initial li, before updating
                    tokenObj, li = __createAToken(fileStr, lineNum, li, xi)
                    if tokenObj:
                        tokenObj.printTokenInfo()
                        #lineNum and xi have to be updated accordingly if comments are multilined
                        if tokenObj._tokenType == 'COMMENT':
                            # if the comments are multilined (e.g., "/* hi\n this is\n*/"), we split the string with the deliminator of the nextline character.
                            splitted = re.split('[\r\n]',tokenObj._tokenStr) #e.g., ["/*", "hi", " this is", "*/"]
                            split_len=len(splitted) # length of the splitted array
                            lineNum=lineNum+(split_len-1) #the lineNumber is updated by adding one less than the length of the splitted array.
                            xi=len(splitted[split_len-1]) #size of the last element of the splitted array is the most updated index of a line.
                        else:
                            xi=xi+(li-li0) #if not multilined comments, update xi.
                        __listOfTokens.append(tokenObj) #append the token created to the list.
                    else:
                        errorStr="!!!ERROR: Invalid token at ["+str(lineNum)+":"+str(xi)+"] >>> "+fileStr[li0:li]
                        print(errorStr)
                        exit()

'''
returns the token object with token info. Also, the function returns one index after the end of the token returned.
'''
def __createAToken(string, lineNum, li, xi):
    length=len(string)
    fi = li + 1  # forward index
    currChar=string[li]
    #tokens that are relational operators (i.e., relop)
    if currChar in ['=','>','<','!','&','|']:
        if currChar == '=':
            fi+=1
            if fi<=length and string[li:fi] == '==':
                return Token('==', tokens_relop['=='], lineNum, xi), fi
            else:
                fi-=1 #go back one index since the token to be returned is "=", not "=="
                return Token('=', tokens_relop['='], lineNum, xi),fi
        elif currChar in ['<','>']:
            fi+=1
            if fi<=length and string[li:fi] in tokens_relop.keys():
                token=string[li:fi]
                return Token(token, tokens_relop[token], lineNum, xi), fi
            else:
                fi-=1
                token=string[li:fi]
                return Token(token, tokens_relop[token], lineNum, xi), fi
        elif currChar== '!':
            fi+=1
            if fi<=length and string[li:fi] == '!=':
                return Token('!=', tokens_relop['!='], lineNum, xi), fi
            else:
                fi-=1
                return Token('!', tokens_relop['!'], lineNum, xi), fi
        elif currChar in ['&','|']:
            fi+=1
            if fi<=length and string[li:fi] in tokens_relop.keys():
                token=string[li:fi] #either && or ||
                return Token(token,tokens_relop[token], lineNum, xi), fi
             #else, do nothing
    #tokens that are operators (e.g., +, -, /) or comments
    elif currChar in tokens_op.keys():
       #check the next character if line[li] is a '/'. If the next character is '*', it is an indication that the following characters are comments.
       if currChar == '/':
           #comments, consisting of a string surrounded by /* and */, without an intervening */, unless it is inside double-quotes(")
           #pattern='/\*([^*"]*|".*"|\*+[^/])*\*/'
           pattern='/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/|(//.*)'
           match=re.match(pattern,string[li:]) # re.match() returns a match object; if no match is found, it returns None
           if match:
               fi=li+match.end() #end index of the matching string
               return Token(string[li:fi],tokens_nonOp['comment'], lineNum, xi), fi
           else:
               return Token('/', tokens_op['/'], lineNum, xi), fi
       else: #other operators
           return Token(currChar, tokens_op[currChar], lineNum, xi), fi

    elif re.match('\d',currChar):
        tokenType='int_const'
        constPattern= '\d+'
        floatPattern= '\d+(\.\d+)+([eE][+-]?\d+)?' #CAVEAT: this only searches positive floating numbers. Scientific notation will also be regarded as a floating point here.
        constMatch= re.match(constPattern, string[li:])
        floatMatch= re.match(floatPattern, string[li:])
        #NOTE: We must first search for the floating point numbers. For example, if the token 1.912 is to be analyzied by matching whole numbers first,
        # 1 will be returned as the token. This is not what we want. In other words, the order of regex search is important!
        if floatMatch:
            fi=li+floatMatch.end()
            return Token(string[li:fi], tokens_nonOp['float_const'], lineNum, xi), fi
        elif constMatch:
            fi=li+constMatch.end()
            return Token(string[li:fi], tokens_nonOp['int_const'], lineNum, xi), fi
        else: #throw error
            return None, -1
    # tokens that are punctuations (e.g., (, {, [, ],))
    elif currChar in tokens_punc.keys():
        return Token(currChar,tokens_punc[currChar],lineNum, xi), fi

    #tokens that are left out (i.e., keywords and ID)
    else:
        pattern=r'[\;\(\{\[,\]\}\)\=\<\>\+\-\*/\!]|\s+'
        while fi<=length and not re.match(pattern,string[fi]):
            fi+=1
        token=string[li:fi]
        #print(f'\"{token}\", fi: {fi}')
        if re.match(r'\bif\b',token):
            return Token(token, tokens_nonOp[token], lineNum, xi),fi
        elif re.match(r'\belse\b',token):
            return Token(token, tokens_nonOp[token], lineNum, xi),fi
        elif re.match(r'\bwhile\b',token):
            return Token(token, tokens_nonOp[token], lineNum, xi),fi
        elif re.match(r'\bint\b',token):
            return Token(token, tokens_nonOp[token], lineNum, xi),fi
        elif re.match(r'\bfloat\b',token):
            return Token(token, tokens_nonOp[token], lineNum, xi),fi
        elif re.match(r'\bprint\b',token):
            return Token(token, tokens_nonOp[token], lineNum, xi),fi
        elif re.match(r'\bread\b',token):
            return Token(token, tokens_nonOp[token], lineNum, xi),fi
        elif re.match(r'\bfunction\b',token):
            return Token(token, tokens_nonOp[token], lineNum, xi),fi
        else:
            return Token(token, tokens_nonOp['identifier'], lineNum, xi), fi

    return None, fi

def getNextToken() -> Token:
    global tokenIndex
    if len(__listOfTokens) == tokenIndex:
        print("[WARNING] Reached the end of the tokens list")
        return None
    nextToken=__listOfTokens[tokenIndex]
    tokenIndex+=1
    return nextToken

def peekNextTokenOf(token:Token) -> Token:
    matchIndex=0
    for t in __listOfTokens:
        if token.equals(t):
            if len(__listOfTokens) == (matchIndex+1):
                print("[WARNING] Reached the end of the tokens list")
                return None
            return __listOfTokens[matchIndex+1]
        matchIndex+=1
    return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("Wrong number of arguments.\n"
                        "\tUSAGE: >> python3 <name_of_the_file.py> <input_file>")
    filename=sys.argv[1]
    __initLexer(filename)

    print("\n====== Testing getNextToken() ======")
    for i in range(6):
        token=getNextToken()
        token.printTokenInfo()

    print("\n====== Printing TokensList======")
    print(f"\tList Length: {len(__listOfTokens)}")
    for i in range(len(__listOfTokens)):
        __listOfTokens[i].printTokenInfo()
else:
    print(f' --- Module \"{__name__}\" is being imported --- ')
    if len(sys.argv) != 2:
        raise Exception("Wrong number of arguments.\n"
                        "\tUSAGE: >> python3 <name_of_the_file.py> <input_file>")
    filename=sys.argv[1]
    __initLexer(filename)
    print(" --- Generated tokens by the lexical analyzer. You may now use getNextToken() --- ")
