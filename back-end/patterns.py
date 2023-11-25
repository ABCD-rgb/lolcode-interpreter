# List of LOLCODE patterns


# === start and end of program ===
codeDelimiters = {
    ("HAI", "Start of Code"),
    ("KTHXBYE", "End of Code"),
}

# ================================


#  === comments ===
comments = {
    ("BTW", "Comment"),
    ("OBTW", "Start of Multiline Comment"),
    ("TLDR", "End of Multiline Comment"),
}

# =================

iKeyword = ("I", "I Keyword") 

# === variables ===
variableSegment = {
    ("WAZZUP", "Start of Variable Declaration"),
    ("BUHBYE", "End of Variable Declaration"),
}

variableDeclaration = {
    ("ITZ", "Variable Initialization"),
}

IhasA = ( "HAS", "A")

variableAssignment = {
    ("R", "Variable Assignment"),
}
# ==================


# === data types ===
yarnLiteral = ("\"([^\"]*)\"", "yarn literal")
numbrLiteral = ("-?[0-9]+", "numbr literal")
numbarLiteral = ("(-)?[0-9]*\.?[0-9]+", "numbar lite")
troofLiteral = ("WIN|FAIL", "troof literal")
typeLiteral = ("NOOB|TROOF|NUMBR|NUMBAR|YARN")
# ==================


# === input/output operations ===
ioKeyword = {
    ("GIMMEH", "input keyword"),
    ("VISIBLE", "output keyword")
}
# ===============================


anSymbol = ("AN", "Conjunction")    # used in many operations


# === arithmetic operations ===
arithmeticOperators = {
    ("SUM", "Addition"),
    ("DIFF", "Subtraction"),
    ("PRODUKT", "Multiplication"),
    ("QUOSHUNT", "Division"),
    ("MOD", "Modulo"),
    ("BIGGR", "Greater Symbol"),
    ("SMALLR", "Lesser Symbol"),
}

arithmeticOf = ("OF")
# =============================


# === concatenation ===
smooshKeyword = ("SMOOSH", "Concatenation Keyword")
# =====================


bothSymbol = ("BOTH")   # used in boolean and comparison operations


# === boolean operations ===
# Boolean Operators - Except Both
booleanOperators = {
    ("EITHER", "or symbol"),
    ("WON", "xor symbol"),
    ("NOT", "not symbol"),
}

booleanOperatorsOf = ("OF")

# Infinite Boolean Operators
infBooleanOperators = {
    ("ALL", "all symbol"),
    ("ANY", "any symbol"),
    ("MKAY", "end of infinite boolean operator"),   
}

infBooleanOperatorsOf = ("OF")
# ==========================




# === comparison operations ===
bothOperators = {
    ("SAEM", "Equality Operator"),
    ("OF", "Comparison Operator"),
}

differentSymbol = ("DIFFRINT", "Inequality")
# =============================


# === typecasting statements ===
castKeyword = {
    ("MAEK", "Typecasting Keyword"),
    ("IS", "Typecasting Keyword"),
    ("A", "Optional Typecasting Keyword"),
}

IsNowA = ("NOW", "A")
IhasA = ("HAS", "A")
# ==============================


# === assignment statements ===
assignmentOperator = {
    ("R", "assignment operator")
}
# ==============================


# === flow-control statements ===
# If-then
ifThenOperator = {
    ("O", "if-then start"),
    ("YA", "if statement"),
    ("NO", "else statement"),
    ("MEBBE", "if-else statament")
}

oRly = "RLY?"
yaRly = "RLY"
noWai = "WAI"

# Switch case
switchCaseOperators = {
    ("WTF?", "switch case start"),
    ("OMG", "case operator"),
    ("OMGWTF", "default case")    
}

endFlowControl = ("OIC", "control flow end")

# Loops
imKeyWord = ("IM", "IM keyword")

loopKeyword = {
    ("IN", "loop start"),
    ("OUTTA", "loop end")
}

yrKeyWord = ("YR", "YR keyword")    # used in loop and function

loopOperationKeyword = {
    ("UPPIN", "increment keyword"),
    ("NERFIN", "decrement keyword")
}

gtfoKeyWord = ("GTFO", "GTFO keyword")  # used in loop and function

loopConditionKeyWord = {
    ("TIL", "loop condition keyword"),
    ("WILE", "loop condition keyword")
}
# ================================


# === function definitions ===
functionKeyWord = ("HOW", "function keyword")

HowIzI = ("Iz", "I")

yrKeyWord = ("YR", "YR keyword")
# ============================


# === function return ===
returnKeyWord = ("FOUND", "return keyword")
# ========================


# === function call ===
Iiz = ("Iz")
# =====================


# === identifiers ===
identifier = ("[a-zA-Z][a-zA-Z0-9_]*", "identifier")
# ===================


