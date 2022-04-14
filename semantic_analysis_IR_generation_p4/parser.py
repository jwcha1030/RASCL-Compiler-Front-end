import lex_v3 as lex
import grammar_globals as gg
import sys

lookahead=lex.getNextToken()

def match(t):
    global lookahead
    if lookahead.getTokenType() == t:
        __printMatchedToken()
        lookahead=lex.getNextToken()
    else:
        syntaxError()

def __printMatchedToken():
    print('\n====== Matched Token: ======')
    lookahead.printTokenInfo()
    print('============================\n')

def syntaxError():
    lineNum = lookahead.getTokenLineNum()
    lineIndex = lookahead.getTokenLineIndex()
    print(f"\nSyntax Error [{lineNum}:{lineIndex}]")

    with open(sys.argv[1],'r') as file:
        lines = file.readlines()
        errorLine = repr(lines[lineNum-1])
        print('>>'+errorLine[1:len(errorLine)-1]) # we must remove the two ' in the front and the end of the line that comes with using repr()
        print(' '*2+' '*(lineIndex-1)+'^') #since a ' is removed at the start 1 is subtracted from the lineIndex
    sys.exit(1)


def printProduction(symbol:str, key=None):
    """
    A auxilary function that prints a symbol's production given such parameter(s):

        symbol(string): a nonterm/terminal to print
        key(string): <optinal; default=None> a key of the symbol's production expressed in a dictionary.
                    This parameter may not be required if there is only one production for the symbol.
    """
    if symbol:
        rhs=eval("gg."+symbol+"_prod")
        if not key:
            print(f"{symbol} -> {rhs[symbol]}")
        else:
            print(f"{symbol} -> {rhs[key]}")
    else:
        argList = [repr(a) if not a else a for a in locals().values()]
        print(f"ERROR: Invalid Parameters provided:\n\tprintProduction({', '.join(argList)})")
        sys.exit(1)


def first(a:dict)->list:
    """
    This function returns a list of FIRST terminals of given symbol's production
        a: dictionary of a symbol's production
        return: a list of First terminals of 'a' symbol.
    """
    firstSymbols=set()
    hasEpsilonProd = True
    terminalFound = False
    def __first_acc(sym:dict):
        nonlocal firstSymbols, hasEpsilonProd, terminalFound
        productions = list(sym.values()) #e.g., ["decl decllist","e"]
        #print(f"Productions: {productions}")
        count=1
        for prodStr in productions:
            terminalFound=False
            hasEpsilonProd=True
            #list of grammar symbol (either nonterminal or terminal) within the product string.
            production = prodStr.split() #e.g., ["decl", "decllist"]
            #print(f"\tProduction {count}: {production}")
            i=0 #index that points to a symbol of a production
            while i<len(production):
                s = production[i]
                #print(f"\t\tEvaluating symbol: {s}")
                if s == 'epsilon': # s is epsilon
                    #print(f"\t\t {s} found!")
                    hasEpsilonProd=True
                    if i < len(production)-1:
                        nextSym = production[i+1]
                        #print(f"\t\t\t Evaluating {s}'s following symbol: {nextSym}")
                        __first_acc(nextSym)
                elif s in gg.terminals and hasEpsilonProd and not terminalFound: #NOTE: gg.terminals does not contain epsilon
                    #print(f"\t\t {s} is a terminal, and it is added to the set: {firstSymbols}")
                    firstSymbols.add(s)
                    terminalFound=True
                    hasEpsilonProd=False
                    break #once the first terminal is found, there is no need to investigate the following symbols.
                elif s not in gg.terminals and hasEpsilonProd and not terminalFound:
                    nonterminal = eval("gg."+s+"_prod") #i.e, gg.decl_prod
                    __first_acc(nonterminal)
                i+=1
            ##end of while loop
            count+=1
        ##end of for loop
    ##end of __first_acc
    __first_acc(a)
    if hasEpsilonProd:
        firstSymbols.add('epsilon')
    return list(firstSymbols)


def parse():
    # find FIRST() for the starting production.
    first_start=first(gg.program_prod)
    #print(f"FIRST(start): {first_start}") #first_start = [INT, FLOAT, FUNCTION, LBRACE]
    printProduction("program")
    while lookahead.getTokenType() != 'DD' :
        decllist()
        funcdecls()
        bstatementlist()
    match('DD')
    # no more token should appear after $$ (i.e., DD)
    if lookahead:
        syntaxError()
    else:
        print("\nSuccessfully parsed!")

def decllist():
    if not lookahead:
        printProduction("decllist", 'e')
        return
    tokenType = lookahead.getTokenType()
    if tokenType == 'INT' or tokenType == 'FLOAT':
        printProduction("decllist")
        decl()
        decllist()
    else: #epsilon
        printProduction('decllist','e')
        return

def decl():
    printProduction("decl")
    typespec()
    variablelist()

def typespec():
    tokenType=lookahead.getTokenType()
    if tokenType == 'INT' or tokenType == 'FLOAT': #either INT or FLOAT
        printProduction('typespec',tokenType.lower())
        match(tokenType)
    else:
        syntaxError()

def variablelist():
    printProduction('variablelist')
    dvariable()
    variablelisttail()

def variablelisttail():
    tokenType= lookahead.getTokenType()
    if tokenType == 'COMMA':
        printProduction('variablelisttail')
        match('COMMA')
        dvariable()
        variablelisttail()
    elif tokenType=='SEMICOLON':
        printProduction('variablelisttail',';')
        match('SEMICOLON')
    else:
        syntaxError()

def dvariable():
    printProduction('dvariable')
    match('ID')
    dvariabletail()

def dvariabletail():
    if not lookahead:
        printProduction('dvariabletail', 'e')
        return
    first_arraydim = first(gg.arraydim_prod)
    #print(f'\tFIRST(arraydim): {first_arraydim}')
    tokenType= lookahead.getTokenType()
    if tokenType in first_arraydim:
        printProduction('dvariabletail')
        arraydim()
    else:
        printProduction('dvariabletail','e')

def arraydim():
    printProduction('arraydim')
    match('LBRACKET')
    arraydimtail()

def arraydimtail():
    printProduction('arraydimtail')
    otherexpression()
    match('RBRACKET')

def otherexpression():
    printProduction('otherexpression')
    term()
    otherexpressiontail()

def otherexpressiontail():
    if not lookahead:
        printProduction('otherexpressiontail','e')
        return

    tokenType= lookahead.getTokenType()
    if tokenType == 'PLUS':
        printProduction('otherexpressiontail','plus')
        match('PLUS')
        term()
        otherexpressiontail()
    elif tokenType=='MINUS':
        printProduction('otherexpressiontail','minus')
        match('MINUS')
        term()
        otherexpressiontail()
    else:
        printProduction('otherexpressiontail','e')

def term():
    printProduction('term')
    factor()
    termtail()

def termtail():
    if not lookahead:
        printProduction('termtail','e')
        return

    tokenType = lookahead.getTokenType()
    if tokenType=='MULT':
        printProduction('termtail','mult')
        match('MULT')
        factor()
        termtail()
    elif tokenType=='DIV':
        printProduction('termtail','div')
        match('DIV')
        factor()
        termtail()
    else:
        printProduction('termtail','e')

def factor():
    tokenType=lookahead.getTokenType()
    if tokenType:
        if tokenType=='ID':
            printProduction('factor','id')
            match('ID')
            factortail()
        elif tokenType == 'ICONST':
            printProduction('factor','iconst')
            match('ICONST')
        elif tokenType == 'FCONST':
            printProduction('factor','fconst')
            match('FCONST')
        elif tokenType=='LPAREN':
            printProduction('factor','parens')
            match('LPAREN')
            otherexpression()
            match('RPAREN')
        elif tokenType=='MINUS':
            printProduction('factor', 'minus')
            match('MINUS')
            factor()
        else:
            syntaxError()
    else:
        syntaxError()

def factortail():
    if not lookahead:
        printProduction('factortail','e')
        return
    first_vartail = first(gg.variabletail_prod) #[epsilon, LBRACKET]
    first_arglist = first(gg.arglist_prod) #[LPAREN]
    #print(f'\tFIRST(variabletail): {first_vartail}')
    #print(f'\tFIRST(arglist): {first_arglist}')
    tokenType = lookahead.getTokenType()
    if tokenType in first_vartail:
        printProduction('factortail','variabletail')
        variabletail()
    elif tokenType in first_arglist:
        printProduction('factortail','arglist')
        arglist()
    else:
        printProduction('factortail','e')

def variable():
    printProduction('variable')
    match('ID')
    variabletail()

def variabletail():
    if not lookahead:
        printProduction('variabletail','e')
        return
    first_arraydim= first(gg.arraydim_prod) #[LBRACKET]
    #print(f'\tFIRST(arraydim): {first_arraydim}')
    if lookahead.getTokenType() in first_arraydim:
        printProduction('variabletail')
        arraydim()
    else:
        printProduction('variabletail','e')

def arglist():
    printProduction('arglist')
    match('LPAREN')
    args()
    match('RPAREN')

def args():
    printProduction('args')
    otherexpression()
    arglisttail()

def arglisttail():
    if not lookahead:
        printProduction('arglisttail','e')
        return
    tokenType=lookahead.getTokenType()
    if tokenType == 'COMMA':
        printProduction('arglisttail')
        match('COMMA')
        otherexpression()
        arglisttail()
    else:
        printProduction('arglisttail','e')

def funcdecls():
    if not lookahead:
        printProduction('funcdecls','e')
        return
    if lookahead.getTokenType() == 'FUNCTION':
        printProduction('funcdecls')
        funcdecl()
        funcdecls()
    else:
        printProduction('funcdecls','e')

def funcdecl():
    printProduction('funcdecl')
    match('FUNCTION')
    typespec()
    functionname()
    paramlist()
    fbody()

def functionname():
    printProduction('functionname')
    match('ID')

def fbody():
    printProduction('fbody')
    match('LBRACE')
    decllist()
    statementlist()
    match('RBRACE')

def paramlist():
    printProduction('paramlist')
    match('LPAREN')
    paramdecllist()
    match('RPAREN')

def paramdecllist():
    printProduction('paramdecllist')
    paramdecl()
    paramdecllisttail()

def paramdecl():
    printProduction('paramdecl')
    typespec()
    dvariable()

def paramdecllisttail():
    if not lookahead:
        printProduction('paramdecllisttail','e')
        return
    if lookahead.getTokenType() == 'COMMA':
        printProduction('paramdecllisttail')
        match('COMMA')
        paramdecl()
        paramdecllisttail()
    else:
        printProduction('paramdecllisttail','e')

def bstatementlist():
    printProduction("bstatementlist")
    match('LBRACE')
    statementlist()
    match('RBRACE')

def statementlist():
    printProduction('statementlist')
    statement()
    statementlisttail()

def statement():
    ##added
    if not lookahead:
        printProduction('statement','e')
        return
    ##
    tokenType = lookahead.getTokenType()
    if tokenType == 'WHILE':
        printProduction('statement','while')
        whilestatement()
    elif tokenType == 'IF':
        printProduction('statement','if')
        ifstatement()
    elif tokenType == 'ID':
        printProduction('statement','assign')
        assignmentexpression()
    elif tokenType == 'PRINT':
        printProduction('statement','print')
        printexpression()
    elif tokenType == 'READ':
        printProduction('statement','read')
        readstatement()
    elif tokenType == 'RETURN':
        printProduction('statement','return')
        returnstatement()
    #else:
        #syntaxError()
    else:
        printProduction('statement','e') #grammar correction

def statementlisttail():
    if not lookahead:
        printProduction('statementlisttail','e')
        return
    if lookahead.getTokenType() == 'SEMICOLON':
        printProduction('statementlisttail')
        match('SEMICOLON')
        statement()
        statementlisttail()
    else:
        printProduction('statementlisttail','e')

def whilestatement():
    printProduction('whilestatement')
    match('WHILE')
    logicalexpr()
    bstatementlist()

def ifstatement():
    printProduction('ifstatement')
    match('IF')
    logicalexpr()
    bstatementlist()
    iftail()

def iftail():
    if not lookahead:
        printProduction('iftail','e')
        return

    if lookahead.getTokenType() == 'ELSE':
        printProduction('iftail')
        match('ELSE')
        bstatementlist()
    else:
        printProduction('iftail','e')

def assignmentexpression():
    printProduction('assignmentexpression')
    variable()
    match('ASSIGN')
    otherexpression()

def printexpression():
    printProduction('printexpression')
    match('PRINT')
    variable()

def printstatement():
    printProduction('printstatement')
    match('PRINT')
    otherexpression()

def readstatement():
    printProduction('readstatement')
    match('READ')
    otherexpression()

def returnstatement():
    printProduction('returnstatement')
    match('RETURN')
    otherexpression()

def logicalexpr():
    printProduction('logicalexpr')
    match('LPAREN')
    condexpr()
    condexprtail()
    logicalexprtail()
    match('RPAREN')

def logicalexprtail():
    if not lookahead:
        printProduction('logicalexprtail','e')
        return

    tokenType=lookahead.getTokenType()
    if tokenType == 'AND':
        printProduction('logicalexprtail', 'and')
        match('AND')
        condexpr()
    elif tokenType == 'OR':
        printProduction('logicalexprtail', 'or')
        match('OR')
        condexpr()
    else:
        printProduction('logicalexprtail','e')

def condexpr():
    tokenType= lookahead.getTokenType()
    first_otherexp = first(gg.otherexpression_prod)
    if tokenType == 'LPAREN':
        printProduction('condexpr','parens')
        #match('LPAREN')
        #otherexpression()
        #condexprtail()
        #match('RPAREN')
        logicalexpr()
    elif tokenType in first_otherexp:
        printProduction('condexpr','otherexpression')
        otherexpression()
        condexprtail()
    elif tokenType == 'NOT':
        printProduction('condexpr','not')
        match('NOT')
        condexpr()
    else:
        syntaxError()

def condexprtail():
    tokenType = lookahead.getTokenType()
    first_relop= first(gg.relop_prod)
    if tokenType in first_relop:
        printProduction('condexprtail')
        relop()
        condexpr()
    else:
        printProduction('condexprtail','e')

def relop():
    tokenType = lookahead.getTokenType()
    if tokenType == 'LT':
        printProduction('relop','lt')
        match('LT')
    elif tokenType == 'GT':
        printProduction('relop','gt')
        match('GT')
    elif tokenType == 'EQ':
        printProduction('relop','eq')
        match('EQ')
    elif tokenType == 'LE':
        printProduction('relop','le')
        match('LE')
    elif tokenType == 'GE':
        printProduction('relop','ge')
        match('GE')
    elif tokenType == 'NE':
        printProduction('relop','ne')
        match('NE')
    else:
        syntaxError()

# test cases for the first() function.
def _test_first():
    print("===== first(start_prod) ======")
    print(f"{first(gg.start_prod)}")
    print("===== first(paramlist_prod) ======")
    print(f"{first(gg.paramlist_prod)}")
    print("===== first(statement_prod) ======")
    print(f"{first(gg.statement_prod)}")
    print("===== first(otherexpression_prod) ======")
    print(f"{first(gg.otherexpression_prod)}")
    print("===== first(arglisttail_prod) ======")
    print(f"{first(gg.arglisttail_prod)}")

    print("===== first(E_prod) ======")
    print(f"{first(gg.E_prod)}")
    print("===== first(Eprime_prod) ======")
    print(f"{first(gg.Eprime_prod)}")
    print("===== first(T_prod) ======")
    print(f"{first(gg.T_prod)}")
    print("===== first(Tprime_prod) ======")
    print(f"{first(gg.Tprime_prod)}")
    print("===== first(F_prod) ======")
    print(f"{first(gg.F_prod)}")


if __name__ == '__main__':
    print("\tParser Initiated")
    #_test_first()
    parse()

