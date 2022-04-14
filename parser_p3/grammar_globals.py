"""
--- Really, a Small C Language(RASCL) GRAMMAR ---

#TOP-DOWN Predictive Recursive Decent Parser

###Start symbol: program
program -> decllist funcdecls bstatementlist DD
funcdecls -> funcdecl funcdecls
funcdecls -> e
funcdecllist -> e
funcdecl -> FUNCTION typespec functionname paramlist fbody
functionname -> ID
paramlist -> LPAREN paramdecllist RPAREN
paramdecllist -> paramdecl paramdecllisttail
paramdecllisttail -> COMMA paramdecl paramdecllisttail
paramdecllisttail -> e
paramdecl -> typespec dvariable
fbody -> LBRACE decllist statementlist RBRACE

decllist -> decl decllist
decllist -> e

bstatementlist -> LBRACE statementlist RBRACE
statementlist -> statement statementlisttail
statementlisttail -> SEMICOLON statement statementlisttail
statementlisttail -> e

decl -> typespec variablelist
variablelist -> dvariable variablelisttail
variablelisttail -> COMMA dvariable variablelisttail
variablelisttail -> SEMICOLON

typespec -> INT
typespec -> FLOAT

dvariable -> ID dvariabletail
dvariabletail -> arraydim
dvariabletail -> e

variable -> ID variabletail
variabletail -> arraydim
variabletail -> e

arraydim -> LBRACKET arraydimtail
arraydimtail -> otherexpression RBRACKET

statement -> whilestatement
statement -> ifstatement
statement -> assignmentexpression
statement -> printexpression
statement -> readstatement
statement -> returnstatement

returnstatement -> RETURN otherexpression

assignmentexpression -> variable ASSIGN otherexpression

printexpression -> PRINT variable

otherexpression -> term otherexpressiontail
otherexpressiontail -> PLUS term otherexpressiontail
otherexpressiontail -> MINUS term otherexpressiontail
otherexpressiontail -> e

term -> factor termtail
termtail -> MULT factor termtail
termtail -> DIV factor termtail
termtail -> e

factor -> ID factortail
factor -> ICONST
factor -> FCONST
factor -> LPAREN otherexpression RPAREN
factor -> MINUS factor
factortail -> variabletail
factortail -> arglist

arglist -> LPAREN args RPAREN
args -> otherexpression arglisttail
arglisttail -> COMMA otherexpression arglisttail
arglisttail -> e

whilestatement -> WHILE logicalexpr bstatementlist

ifstatement -> IF logicalexpr bstatementlist iftail
iftail -> ELSE bstatementlist
iftail -> e

logicalexpr -> condexpr logicalexprtail
logicalexprtail -> AND condexpr
logicalexprtail -> OR condexpr
logicalexprtail -> e
condexpr -> LPAREN otherexpression condexprtail RPAREN
condexpr -> otherexpression condexprtail
condexpr -> NOT condexpr
condexprtail -> relop otherexpression
relop -> LT | GT | EQ | LE | GE | NE

printstatement -> PRINT otherexpression
readstatement -> READ otherexpression
"""
terminals=["ASSIGN", "LT", "LE", "GT", "GE", "EQ", "NE", "NOT", "AND", "OR",
        "PLUS", "MINUS", "MULT", "DIV", "SEMICOLON", "LPAREN", "RPAREN", "COMMA",
        "LBRACE", "RBRACE", "LBRACKET", "RBRACKET", "IF", "ELSE", "WHILE", "INT",
        "FLOAT", "ID", "ICONST", "FCONST", "PRINT", "READ", "FUNCTION", "RETURN", "DD"]

#START
program_prod={"program":"decllist funcdecls bstatementlist DD"}
#function
funcdecls_prod={'funcdecls': 'funcdecl funcdecls', 'e':'epsilon'}
funcdecl_prod = {'funcdecl': 'FUNCTION typespec functionname paramlist fbody'}
functionname_prod = {'functionname':'ID'}
fbody_prod = {'fbody': 'LBRACE decllist statementlist RBRACE'}
#parameters
paramlist_prod = {'paramlist': 'LPAREN paramdecllist RPAREN'}
paramdecllist_prod ={'paramdecllist': 'paramdecl paramdecllisttail'}
paramdecl_prod = {'paramdecl': 'typespec dvariable'}
paramdecllisttail_prod = {'paramdecllisttail': 'COMMA paramdecl paramdecllisttail', 'e': 'epsilon'}
#statement list
bstatementlist_prod = {'bstatementlist':'LBRACE statementlist RBRACE'}
statementlist_prod= {'statementlist': 'statement statementlisttail'}
statementlisttail_prod = {'statementlisttail': 'SEMICOLON statement statementlisttail', 'e':'epsilon'}
#declarations
decllist_prod = {'decllist': 'decl decllist', 'e': 'epsilon'}
decl_prod = {'decl': 'typespec variablelist'}
#declaration variable list
variablelist_prod ={'variablelist': 'dvariable variablelisttail'}
variablelisttail_prod = {'variablelisttail': 'COMMA dvariable variablelisttail', ';':'SEMICOLON'}
dvariable_prod={'dvariable':'ID dvariabletail'}
dvariabletail_prod={'dvariabletail':'arraydim','e':'epsilon'}
#types
typespec_prod={'int':'INT', 'float':'FLOAT'}
#variable
variable_prod = {"variable":"ID variabletail"}
variabletail_prod = {'variabletail':'arraydim', 'e':'epsilon'}
#array dimensions
arraydim_prod = {'arraydim':'LBRACKET arraydimtail'}
arraydimtail_prod = {'arraydimtail':'otherexpression RBRACKET'}
#statement
statement_prod = {'while':'whilestatement', 'if':'ifstatement',
        'assign':'assignmentexpression', 'print':'printexpression', 'read':'readstatement',
        'return':'returnstatement', 'e':'epsilon'}
returnstatement_prod = {'returnstatement':'RETURN otherexpression'}
whilestatement_prod = {'whilestatement':'WHILE logicalexpr bstatementlist'}
ifstatement_prod = {'ifstatement':'IF logicalexpr bstatementlist iftail'}
iftail_prod = {'iftail':'ELSE bstatementlist', 'e':'epsilon'}
printexpression_prod={'printexpression':'PRINT variable'}
readstatement_prod = {'readstatement': 'READ otherexpression'}
#expressions
assignmentexpression_prod = {'assignmentexpression': 'variable ASSIGN otherexpression'}
printstatement_prod = {'printstatement': 'PRINT otherexpression'}
otherexpression_prod = {'otherexpression': 'term otherexpressiontail'}
otherexpressiontail_prod={'plus': 'PLUS term otherexpressiontail', 'minus':'MINUS term otherexpressiontail', 'e':'epsilon'}
logicalexpr_prod = {'logicalexpr':'condexpr logicalexprtail'}
logicalexprtail_prod = {'and':'AND condexpr', 'or':'OR condexpr', 'e':'epsilon'}
condexpr_prod = {'parens':'LPAREN otherexpression condexprtail RPAREN', 'otherexpression':'otherexpression condexprtail', 'not':'NOT condexpr'}
condexprtail_prod = {'condexprtail':'relop otherexpression'}
relop_prod = {'lt':'LT', 'gt':'GT','eq':'EQ', 'le':'LE', 'ge':'GE', 'ne':'NE'}
#terms
term_prod = {'term': 'factor termtail'}
termtail_prod = {'mult': 'MULT factor termtail', 'div': 'DIV factor termtail', 'e':'epsilon'}
#factor
factor_prod = {'id':'ID factortail', 'iconst':'ICONST', 'fconst':'FCONST', 'parens':'LPAREN otherexpression RPAREN', 'minus': 'MINUS factor'}
factortail_prod = {'variabletail':'variabletail', 'arglist':'arglist', 'e':'epsilon'}
#argument list
arglist_prod = {'arglist':'LPAREN args RPAREN'}
args_prod = {'args': 'otherexpression arglisttail'}
arglisttail_prod = {'arglisttail':'COMMA otherexpression arglisttail', 'e':'epsilon'}

##for testing purpose. Grammar below is not related to RASCL
E_prod = {'e':"T Eprime"}
Eprime_prod = {'plus':"PLUS T Eprime", 'ep':'epsilon'}
T_prod = {'t':"F Tprime"}
Tprime_prod = {'mult':"MULT F Tprime", 'ep':'epsilon'}
F_prod = {'f':'LPAREN E RPAREN', 'id': 'ID'}

