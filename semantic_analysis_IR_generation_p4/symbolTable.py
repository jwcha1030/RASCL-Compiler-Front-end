# David Cha CSE304 PhaseII
import sys
import os

#lexPath=os.path.abspath('../Phase1/lex.py')
#lex_dir=os.path.dirname(lexPath)
#sys.path.append(os.path.split(lex_dir)[0])
#from Phase1 import lex

typeInfo={1:'integer', 2: 'float', 3: 'array', 4: 'string', -1: 'None'}
attributeInfo={'identifier':0, 'symType':1, 'memAddr':2, 'scope':3}
tableSize = 11
hashTable = [[] for i in range(tableSize)]

# 0: pervasive, 1: global(user's), 2: scope of function1, 3: scope of function2...
scopeStack = [0]
lastUsedScope=0

class SymbolInfo():
    def __init__(self, identifier:str, symType: int, scope:int):
        '''
        identifier: a string representation of the symbol
        symType: the type of the symbol represented by integers (e.g. integer-> 1, float -> 2)
        memAddr: the memory address of the symbol represented as "identity" object using built-in function id()
        scope: the scope, represented in integers, that the symbol resides
        '''
        self.identifier=identifier
        self.symType=symType
        self.memAddr=hex(id(self)) # placeholder is the memory address of this object
        self.scope=scope

    def printSymbolInfo(self):
        attrs=vars(self)
        printStr=[]
        for key in attrs:
            if key=="symType":
                printStr.append(f"{key}: {typeInfo[attrs[key]]}")
            elif key=="identifier":
                printStr.append(f"{key}: {repr(attrs[key])}")
            else:
                printStr.append(f"{key}: {attrs[key]}")
        print(', '.join(printStr))

    def getId(self):
        return self.identifier

    def getSymType(self):
        return self.symType

    def getMemAddr(self):
        return self.memAddr

    def getSymScope(self):
        return self.scope

    def __str__(self):
        return "{ "+repr(self.identifier) + "@" + self.memAddr+" }"

def _insertToHashTable(symbol:SymbolInfo):
    name=symbol.getId()
    index=_hashIndex(name)
    #print(f"\tString: {repr(name)}, HashCode:{hashCode}, TableIndex:{index}")
    hashTable[index].append(symbol)

def _hashIndex(name:str)-> int:
    hashCode=hash(name)
    index=hashCode % tableSize
    return index

def _printHashTable():
    for i in range(len(hashTable)):
        entryLength = len(hashTable[i])
        print(f"Index {i} Length: {entryLength}")
        entry=""
        for j in range(entryLength):
            entry+=(" "+str(hashTable[i][j])+", ") if j != entryLength-1 else (str(hashTable[i][j])+" ")
        print(f"\t[{entry}]")

def initSymTable():
    """
    Initializes the symbol table manager
    """
    print(">> initSymTable()")
    global lastUsedScope
    #NOTE: global scope is 1 (not 0 as is in the instructions).
    # I wanted to add the pervasive scope for later use and implementations.
    lastUsedScope=globalScope = 1 #user accessed global scope
    scopeStack.append(globalScope) #push the outermost scope
    '''
    #takes tokens with type ID and puts them into the symbol table.
    token=lex.getNextToken()
    while token:
        if token.getTokenType() =='ID':
            symbol=_createSymbolFromToken(token)
            _insertToHashTable(symbol)
        token=lex.getNextToken()
    '''
    #_printHashTable()

def _createSymbolFromToken(token) -> SymbolInfo:
    identifier = token.getTokenStr()
    symType= -1 #placeholder
    scope = -1
    return SymbolInfo(identifier, symType, scope)

#top of the scope stack
def _currentScope()->int:
    topIndex= len(scopeStack)-1
    return scopeStack[topIndex]

# enterScope() increments lastUsedScope.
def enterScope()->int:
    print(">> enterScope()")
    global lastUsedScope
    lastUsedScope = newScope = lastUsedScope + 1
    scopeStack.append(newScope)
    return  newScope

#NOTE: calling exitScope() should not update lastUsedScope(i.e.,  Exiting from a scope should not remove a function's scope)
def exitScope():
    print(">> exitScope()")
    if len(scopeStack)<=2: # 2 because of pervasive scope
        print("Error: Scope stack empty")
        exit()
    print(f"Exited from the current scope {_currentScope()}.")
    scopeStack.pop(_currentScope())

def addSymbol(identifier:str) -> bool:
    '''
    Adds a SymbolInfo object to the hashtable for the symbol identifier. Initially, the SymbolInfo object only contains
    the identifier itself (other attributes with placeholders). The function returns if the identifier was successfully
    added to the table, false, otherwise.

    Parameters:
        identifier: str
            symbol name in string
    '''
    argList=[str(val) for val in locals().values()]
    print(f">> addSymbol({', '.join(argList)})")
    if not symbolInTable(identifier,_currentScope(),0):
        # -1 is a placeholder for both symType
        newSymbol= SymbolInfo(identifier, -1, _currentScope())
        _insertToHashTable(newSymbol)
        return True
    return False

def addAttributeToSymbol(identifier:str, scope:int, attr:int, value) -> bool:
    '''
    Locates the identifier in the requested scope and adds a new attribute to the symbol information with the provided
    value. If the function is called additional times with the same attribute parameter, the function should overwrite
    the old value for that attribute. If the function successfully finds the symbol and adds or changes the attribute,
    it returns true. If the function does not find the symbol or the other parameters are bad, it returns false.

    Parameters:
        identifier:str
            symbol name in string
        scope:int
            scope of symbol to be searched.(>0)
        attr:int
            symbol's attribute to be updated.
        value:void
            value of the provided attribute. if the attribute is symType and its type is an array, the value must be a tuple of (3, [dimensions,...]).
            3 represents an array, [dimensions,..] represents a list of upper index bounds of the array.
    '''
    argList=[str(val) for val in locals().values()]
    print(f">> addAtributeToSymbol({', '.join(argList)})")
    if scope < 0:
        print(f"ERROR: scope {scope} is not valid")
        return False

    symbolFound=getSymbol(identifier, scope, 0)
    if symbolFound:
        attrName=""
        for key, val in attributeInfo.items():
            if val == attr:
                attrName=key
            try:
                if attrName=="memAddr":
                    setattr(symbolFound, attrName, hex(value))
                    return True
                elif attrName=="symType":
                    if isinstance(value,tuple) and len(value)==2:
                        setattr(symbolFound, attrName, value[0])
                        setattr(symbolFound, "dimension", len(value[1]))
                        setattr(symbolFound, "dimension_bounds", value[1])
                        return True
                    else:
                        setattr(symbolFound, attrName, value)
                        return True
                elif attrName:
                    setattr(symbolFound, attrName, value)
                    return True
            except:
                print(f"ERROR: attribute {attrName} cannot be set to {symbolFound}")
                return False
    return False

def symbolInTable(identifier:str, scope:int, printInfo=1) -> bool:
    '''
    Verifies an identifier is in the table. It returns true if it is and false otherwise.
    The symbol is searched for in the provided scope. If scope is negative, the symbol is searched
    for any scope.

    Parameters:
        identifier:str
            symbol name in string
        scope:int
            scope of symbol to be searched (negative to search in any scope)
        printInfo: int
            add 0 to disable printing the function name and the argument list
    '''
    if printInfo:
        argList=[str(val) for val in locals().values()]
        print(f">> symbolInTable({', '.join(argList)})")
    i = _hashIndex(identifier)
    for symbol in hashTable[i]:
        if symbol.getId()==identifier:
            if scope<0:
                return True
            elif scope >= 0 and symbol.getSymScope()==scope:
                return True
    return False

def getSymbol(identifier:str, scope:int, printInfo=1)-> SymbolInfo:
    '''
    Locates the SymbolInfo class for the named identifier. It returns the SymbolInfo
    record if the symbol is found in the scope provided (global if scope=1). It returns None otherwise.

    Parameters:
        identifier:str
            symbol name in string
        scope:int
            scope of symbol to be searched.
        printInfo: int
            add 0 to disable printing the function name and the argument list
    '''
    if printInfo:
        argList=[str(val) for val in locals().values()]
        print(f">> getSymbol({', '.join(argList)})")
    i = _hashIndex(identifier)
    for symbol in hashTable[i]:
        if symbol.getId()==identifier and symbol.getSymScope()==scope:
            return symbol
    return None

def retrieveSymbol(identifier:str):
    argList=[str(val) for val in locals().values()]
    print(f">> retrieveSymbol({', '.join(argList)})")
    symbol=getSymbol(identifier, _currentScope(), 0)
    symbol.printSymbolInfo()

def __runTest():
    print(f" --- Testing the Symbol Table --- ")
    print("!!Note that global scope is set as 1 not 0")
    addSymbol("temperature") #2
    addSymbol("velocity") #2
    addSymbol("temp") #2
    addAttributeToSymbol("temperature",_currentScope(),attributeInfo['symType'], 1) #3
    addAttributeToSymbol("velocity",_currentScope(),attributeInfo['symType'], 1) #3

    print("New scope entered:",enterScope()) #4

    addSymbol("velocity") #5
    addSymbol("position") #5
    addAttributeToSymbol("velocity",_currentScope(), attributeInfo['symType'], 2) #6
    addAttributeToSymbol("position",_currentScope(), attributeInfo['symType'], 1) #7
    #8
    if symbolInTable("temperature",-1):
        print("temperature is in the symbol table")
    else:
        print("temperature is NOT in the symbol table")
    #9
    if symbolInTable("bang",-1):
        print("bang is in the symbol table")
    else:
        print("bang is NOT in the symbol table")
    retrieveSymbol("position")#10
    exitScope() #11
    addAttributeToSymbol("temperature",_currentScope(), attributeInfo['memAddr'],0x800000) #12a
    addAttributeToSymbol("velocity",_currentScope(), attributeInfo['memAddr'],0x800020) #12b
    addAttributeToSymbol("temp",_currentScope(), attributeInfo['symType'],(3, [15,10])) #12ci
    addAttributeToSymbol("temp",_currentScope(), attributeInfo['memAddr'], 0x800040) #12cii
    retrieveSymbol("temp") #check
    #13
    symbolFound=getSymbol("temperature", _currentScope())
    if symbolFound:
        symbolFound.printSymbolInfo()
    else:
        print(f"temperature is not found in the symbol table in scope {_currentScope()}.")
    #14
    symbolFound2=getSymbol("velocity", 2)
    if symbolFound2:
        symbolFound2.printSymbolInfo()
    else:
        print(f"velocity (scope 2) is not found in the symbol table")
    #15
    symbolFound3=getSymbol("position", 2)
    if symbolFound3:
        symbolFound3.printSymbolInfo()
    else:
        print(f"position (scope 2) is not found in the symbol table")
    #16
    symbolFound4=getSymbol("velocity",1)
    if symbolFound4:
        symbolFound4.printSymbolInfo()
    else:
        print(f"velocity (global scope) is not found in the symbol table")
    #17
    symbolFound5=getSymbol("bang",_currentScope())
    if symbolFound5:
        symbolFound4.printSymbolInfo()
    else:
        print(f"bang (global scope) is not found in the symbol table")

if __name__ == '__main__':
    print(f" --- Initializing the Symbol Table --- ")
    initSymTable()
    __runTest()
   #_printHashTable()
