import re  # Regular expressions
import patterns

class Lexeme:
    def __init__(self, regex, token_type):
        self.regex = regex
        self.token_type = token_type

    def __repr__(self):  # For debugging
        return f"Lexeme({self.regex}, {self.token_type})"

def main():
    # lexemes = [
    #     Lexeme(r"HAI", "Code Delimiter"),
    #     Lexeme(r"KTHXBYE", "Code Delimiter"),
    #     Lexeme(r"I HAS A", "Variable Declaration"),
    #     Lexeme(r"ITZ", "Variable Assignment"),
    #     Lexeme(r"VISIBLE", "Output"),
    #     Lexeme(r"\"", "String Delimiter"),  # Updated regex for string delimiter
    #     # Catch all the characters between the string delimiters using named groups
    #     Lexeme(r"(?P<string>.*?)(?P=string)", "String Literal"),
    #     # Catch the string delimiter after the string literal
    #     Lexeme(r"\"", "String Delimiter"),
    #     Lexeme(r"[a-zA-Z][a-zA-Z0-9_]*", "Variable Name"),
    #     Lexeme(r"-?[0-9]+", "Integer Literal"),
    #     Lexeme(r"(-)?[0-9]*\.?[0-9]+", "Float Literal"),
    #     # Catch newlines
    # ]

    # # Identify tokens
    # tokens = []
    # with open("test.lol", "r") as f:
    #     f = f.read().splitlines()
    #     f = [line.strip() for line in f]    # remove traling and leading spaces
    #     print(f"{f}\n")
    #     for line in f:
    #         position = 0
    #         for lexeme in lexemes:
    #             match = re.search(lexeme.regex, line[position:])
    #             if match:
    #                 start, end = match.span()
    #                 position += end  # Move the position after the matched portion
    #                 tokens.append((match.group(0), lexeme.token_type))

    # # Print tokens
    # for token in tokens:
    #     print(token)


    # Remove comments BTW, OBTW, TLDR
    with open("test.lol", "r") as f:
        f = f.read().splitlines()
        f = [line.strip() for line in f]    # remove traling and leading spaces 

        clean_string = ""
        isComment = False
        
        for line in f:
            # If OBTW is found, remove the rest of the lines until TLDR is found
            if (re.search("OBTW", line)):
                line = re.sub("OBTW", "", line)
                isComment = True
            
            
            if (isComment):
                if (re.search("TLDR", line)):
                    line = re.sub("TLDR.*", "", line)
                    isComment = False
                else:
                    line = ""
                
            # If TLDR is found, remove the rest of the line
            if (re.search("TLDR", line)):
                line = re.sub("TLDR.*", "", line)
            
            # If BTW is found, remove the rest of the line
            if (re.search("BTW", line)):
                line = re.sub("BTW.*", "", line)
          
            if (line != ""):
                clean_string += line + "\n"
                
    print(f"clean string:\n{clean_string}\n")
    
    # tokenize
    tokens = []
    curr_keyword = ""                
    string_flag = False     # to catch strings
    for letter in clean_string:
        if not string_flag:
            if letter == '"':
                string_flag = True
                tokens.append(letter)
            elif letter == " " or letter == "\n":
                if curr_keyword != "":
                    tokens.append(curr_keyword)
                    curr_keyword = ""
                if letter == "\n":
                    next
            else:
                curr_keyword += letter
        else:
            if letter == '"':
                string_flag = False
                tokens.append(curr_keyword)
                curr_keyword = ""
                tokens.append(letter)
            else:
                curr_keyword += letter

    print(tokens)

    # identify classification of tokens

if __name__ == "__main__":
    main()
