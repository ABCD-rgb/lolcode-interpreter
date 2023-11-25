# Authors:
#   Tyrone Frederik Nagano
#   Edgar Go
# Section: CMSC 124 T-2L
# Date Created: November 15, 2022

# This contains the Regex for the lexemes

# Paired Keywords
pairedKeywords = {
    ('HAI', 'start program keyword'),
    ('KTHXBYE', 'end program keyword'),
    ('OBTW', 'start multiline comment'),
    ('TLDR', 'end multiline comment')
}

# Arithmetic keyword
arithmeticKeyword = {
    ('SUM', 'addition operator'),
    ('DIFF', 'subtraction operator'),
    ('PRODUKT', 'multiplication operator'),
    ('QUOSHUNT', 'divition operator'),
    ('MOD', 'modulo operator'),
    ('BIGGR', 'max operator'),
    ('SMALLR', 'min operator')
}

# Concat operators
concatenationOperator = {
    ('SMOOSH', 'concatenation operator')
}

# Boolean operator
booleanUnaryOperator = {
    ('NOT', 'logical not operator')
}

bothKeyword = 'BOTH'

bothOperator = {
    ('SAEM', 'comparison equal to operator'),
    ('OF', 'logical and operator')
}

booleanOperator = {
    ('EITHER', 'logical or operator'),
    ('WON', 'logical xor operator'),
}

# Followed by an OF and has MKAY as delimiter
booleanInfArOperator = {
    ('ANY', 'logical or operator with infinite arity'),
    ('ALL', 'logical and operator with infinite arity')
}

# Boolean operation with infinite arity
booleanInfArMkay = ('MKAY', 'end of boolean operator with infinite arity')

# Arithmetic operation must be followed by an OF
operatorOf = 'OF'
operatorAn = ('AN', 'operand separator')

# Comparison operator
comparisonOperator = {
    ('DIFFRINT', 'comparison not equal to operator')
}

# Variable initialization
variableInitializationOperator = {
    ('I', 'variable declaration'),
    ('ITZ', 'variable initialization')
}

# Typecasting variable (note: does not change the actual value but changes the type of the return value)
# Value will be stored at IT
typecastOperator = {
    ('MAEK', 'typecast operator'),
    ('IS', 'typecast operator'),
    ('A', 'optional keyword after MAEK')
}

# IS keyword must be followed by a 'NOW A'
isNowA = ('NOW', 'A')

# I operator must be followed by 'HAS A'
iHasA = ('HAS', 'A')

# Assignment operator
assignmentOperator = {
    ('R', 'assignment operator'),
}

# Control Flow Operators
ifThenwOperator = {
    ('O', 'start of if-then statement'),
    ('YA', 'if statement'),
    ('NO', 'else statement'),
    ('MEBBE', 'if-else clause')
}

oRly = 'RLY?'
yaRly = 'RLY'
noWai = 'WAI'

# Switch case statements
switchCaseOperators = {
    ('WTF?', 'start of switch case statement'),
    ('OMG', 'case operator'),
    ('OMGWTF', 'default case')
}

endOfFlowControl = ('OIC', 'end of if-then statement'),

# Loop Statement
imKeyword = 'IM'

loopKeyword = {
    ('IN', 'start of loop'),
    ('OUTTA', 'end of loop')
}

yrKeyword = ('YR', 'loop keyword')

loopOperationKeyword = {
    ('UPPIN', 'increment keyword'),
    ('NERFIN', 'decrement keyword')
}

breakKeyword = ('GTFO', 'break keyword')

loopConditionKeyword = {
    ('TIL', 'loop condition keyword'),
    ('WILE', 'loop condition keyword')
}

# I/O Keywords
ioKeyword = {
    ('GIMMEH', 'input keyword'),
    ('VISIBLE', 'output keyword')
}

# LITERALS
yarnLiteral = ('^".*"$', 'yarn literal')
numbrLiteral = ('^-?[0-9]+$', 'numbr literal')
numbarLiteral = ('^-?[0-9]*\\.[0-9]+$', 'numbar literal')
troofLiteral = ('^WIN$|^FAIL$', 'troof literal')
typeLiteral = ('^TROOF$|^NOOB$|^NUMBR$|^NUMBAR$|^YARN$|^TYPE$', 'type literal')

# IDENTIFIER
# need to distinguish between function, variable, loop
generalIdentifier = ('[A-Za-z][A-Za-z0-9_]*', 'general identifier')
