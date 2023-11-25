# Authors:
#   Tyrone Frederik Nagano
#   Edgar Go
# Section: CMSC 124 T-2L
# Date Created: November 15, 2022

import re
from Regex import *

# Function to tokenize the source code

# Lexical analyzer function


def lexer(source_code):

    string_flag = False
    comment_flag = False
    token_found = False
    tokens = []
    word = []
    string = []
    with open(source_code) as f:
        while True:
            char = f.read(1)
            # If whitespace or newline is encountered, check if string_flag is false
            if char == "\n" or char.isspace() or (not char):
                if string_flag == False:
                    if len(word) != 0:
                        # If string_flag is false, join characters together to form a keyword
                        keyword = ''.join(word)
                        # print(keyword)
                        word = []                               # Clear the word array
                        if keyword == "BTW":
                            # If a BTW is encountered, set comment flag to true to prevent characters being read until a newline
                            comment_flag = True
                        else:
                            tokens.append(keyword)
                    if char == "\n":
                        comment_flag = False
                    if not char:                                # Break if it is already EOF
                        break
                else:
                    # If string_flag is true, append the space or newline to the string
                    string.append(char)
            elif char == "\"":
                if comment_flag != True:
                    # If quotes are encountered, set the string_flag to the opposite of its current state
                    if string_flag == False:
                        tokens.append(char)
                        string_flag = True
                    else:
                        # Setting the string_flag from True to False will join the characters of the string together
                        string_flag = False
                        string_join = ''.join(string)
                        tokens.append(string_join)
                        tokens.append(char)
                        string = []                                 # Clear the string array
            else:
                if comment_flag != True:
                    if string_flag == False:                        # All other characters will be appended to the word array if the flag is false. If it is true, append to the string array
                        word.append(char)
                    else:
                        string.append(char)

    print(tokens)
    symbol_table = []
    i = 0
    # Loop through all the tokens
    while i < len(tokens):
        # Check if it exists in all the dictionary of tuples,
        for item in pairedKeywords:
            # and if it does, append it to the symbol table array
            if tokens[i] == item[0]:
                # as a tuple. Tuple consists of the token and its classification.
                symbol_table.append((tokens[i], item[1]))
                token_found = True
                break
        for item in arithmeticKeyword:
            if tokens[i] == item[0]:
                if tokens[i + 1] == operatorOf:
                    symbol_table.append(
                        ((tokens[i] + " " + tokens[i + 1]), item[1]))
                    token_found = True
                    i += 1
                    break
        for item in concatenationOperator:
            if tokens[i] == item[0]:
                symbol_table.append((tokens[i], item[1]))
                token_found = True
                break
        for item in booleanUnaryOperator:
            if tokens[i] == item[0]:
                symbol_table.append((tokens[i], item[1]))
                token_found = True
                break
        for item in booleanOperator:
            if tokens[i] == item[0]:
                if tokens[i + 1] == operatorOf:
                    symbol_table.append(
                        ((tokens[i] + " " + tokens[i + 1]), item[1]))
                    token_found = True
                    i += 1
                    break
        for item in booleanInfArOperator:
            if tokens[i] == item[0]:
                if tokens[i + 1] == operatorOf:
                    symbol_table.append(
                        ((tokens[i] + " " + tokens[i + 1]), item[1]))
                    token_found = True
                    i += 1
                    break
        for item in variableInitializationOperator:
            if tokens[i] == item[0]:
                if tokens[i + 1] == iHasA[0] and tokens[i + 2] == iHasA[1]:
                    symbol_table.append(
                        ((tokens[i] + " " + tokens[i + 1] + " " + tokens[i + 2]), item[1]))
                    token_found = True
                    i += 2
                    break
                else:
                    symbol_table.append((tokens[i], item[1]))
                    token_found = True
                    break
        for item in typecastOperator:
            if tokens[i] == item[0]:
                if tokens[i + 1] == isNowA[0] and tokens[i + 2] == isNowA[1]:
                    symbol_table.append(
                        ((tokens[i] + " " + tokens[i + 1] + " " + tokens[i + 2]), item[1]))
                    token_found = True
                    i += 2
                    break
                else:
                    if item[0] == "A":
                        if tokens[i - 1] != iHasA[0] and tokens[i - 1] != isNowA[0]:
                            symbol_table.append((tokens[i], item[1]))
                            token_found = True
                            break
                    else:
                        symbol_table.append((tokens[i], item[1]))
                        token_found = True
                        break
        for item in assignmentOperator:
            if tokens[i] == item[0]:
                symbol_table.append((tokens[i], item[1]))
                token_found = True
                break
        for item in ifThenwOperator:
            if tokens[i] == item[0]:
                if item[0] == "O":
                    if tokens[i + 1] == oRly:
                        symbol_table.append(
                            ((tokens[i] + " " + tokens[i + 1]), item[1]))
                        token_found = True
                        i += 1
                        break
                elif item[0] == "YA":
                    if tokens[i + 1] == yaRly:
                        symbol_table.append(
                            ((tokens[i] + " " + tokens[i + 1]), item[1]))
                        token_found = True
                        i += 1
                        break
                elif item[0] == "NO":
                    if tokens[i + 1] == noWai:
                        symbol_table.append(
                            ((tokens[i] + " " + tokens[i + 1]), item[1]))
                        token_found = True
                        i += 1
                        break
                else:
                    symbol_table.append(((tokens[i]), item[1]))
                    token_found = True
                    break
        for item in switchCaseOperators:
            if tokens[i] == item[0]:
                symbol_table.append((tokens[i], item[1]))
                token_found = True
                break
        for item in endOfFlowControl:
            if tokens[i] == item[0]:
                symbol_table.append((tokens[i], item[1]))
                token_found = True
                break
        for item in comparisonOperator:
            if tokens[i] == item[0]:
                symbol_table.append((tokens[i], item[1]))
                token_found = True
                break
        for item in loopOperationKeyword:
            if tokens[i] == item[0]:
                symbol_table.append((tokens[i], item[1]))
                token_found = True
                break
        for item in loopConditionKeyword:
            if tokens[i] == item[0]:
                symbol_table.append((tokens[i], item[1]))
                token_found = True
                break
        for item in ioKeyword:
            if tokens[i] == item[0]:
                symbol_table.append((tokens[i], item[1]))
                token_found = True
                break
        if tokens[i] == operatorAn[0]:
            symbol_table.append((tokens[i], operatorAn[1]))
            token_found = True
            
        if tokens[i] == booleanInfArMkay[0]:
            symbol_table.append((tokens[i], booleanInfArMkay[1]))
            token_found = True
            
        if tokens[i] == bothKeyword:
            for operator in bothOperator:
                if tokens[i + 1] == operator[0]:
                    symbol_table.append(
                        ((tokens[i] + " " + tokens[i + 1]), operator[1]))
                    token_found = True
                    i += 1
                    break
        if tokens[i] == imKeyword:
            for keyword in loopKeyword:
                if tokens[i + 1] == keyword[0] and tokens[i + 2] == yrKeyword[0]:
                    symbol_table.append(
                        ((tokens[i] + " " + tokens[i + 1] + " " + tokens[i + 2]), keyword[1]))
                    token_found = True
                    i += 2
                    break
        if tokens[i] == "\"":
            symbol_table.append((tokens[i], "string delimiter"))
            token_found = True
        if tokens[i-1] == "\"" and tokens[i+1] == "\"":
            symbol_table.append((tokens[i], "string literal"))
            token_found = True
        if tokens[i] == yrKeyword[0]:
            symbol_table.append((tokens[i], yrKeyword[1]))
            token_found = True
        if tokens[i] == breakKeyword[0]:
            symbol_table.append((tokens[i], breakKeyword[1]))
            token_found = True
            
        # pattern = re.compile(numbrLiteral[0])
        # if pattern.match(tokens[i]) == True:
        #     symbol_table.append((tokens[i], numbrLiteral[1]))
        if not token_found:
            search = re.search(numbrLiteral[0], tokens[i])
            if search == None:
                search = re.search(numbarLiteral[0], tokens[i])
                if search == None:
                    search = re.search(troofLiteral[0], tokens[i])
                    if search == None:
                        search = re.search(typeLiteral[0], tokens[i])
                        if search != None:
                            # Type Literal
                            symbol_table.append((tokens[i], typeLiteral[1]))
                            token_found = True
                    else:
                        # Troof literal
                        symbol_table.append((tokens[i], troofLiteral[1]))
                        token_found = True
                else:
                    # Numbar literal
                    symbol_table.append((tokens[i], numbarLiteral[1]))
                    token_found = True
            else:
                # Numbr literal
                symbol_table.append((tokens[i], numbrLiteral[1]))
                token_found = True
        if not token_found:
            search = re.search(generalIdentifier[0], tokens[i])
            if search != None:
                symbol_table.append((tokens[i], generalIdentifier[1]))
                token_found = True
        
        token_found = False
        i+=1
    for pair in symbol_table:
        print("===KEYWORD: ", pair[0], "     CLASSIFICATION: ", pair[1])

# Test
file_name = "code.lol"
lexer(file_name)
