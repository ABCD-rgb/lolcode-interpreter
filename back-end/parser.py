import patterns as p
import lexer as l


lexemes = l.lexer("parser_test.lol")

class ParseNode:
    def __init__(self, data, parent=None):
        self.parent = None
        self.data = data
        self.children = []
    
        
    def __str__(self):
        tree = ''
        
        # Generate the tree and return it
        tree += self.data.keyword + '\n'
        if self.first_child:
            tree += self.first_child.__str__()
        if self.next_sibling:
            tree += self.next_sibling.__str__()
            
        return tree
    
def print_tree(node, indent=0, prefix=''):
    if node is not None:
        print(' ' * indent + prefix + node.data.keyword)
        print_tree(node.first_child, indent + 4, "|-- ")
        print_tree(node.next_sibling, indent, prefix)


# print(lexemes)
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.parse_tree = None
        
        self.advance()
        
    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok
    
    def parse(self):
        res = self.program()
        return res
    
    
    def program(self):
        tok = self.current_tok
        
        # If the token is HAI then we can continue
        if tok.keyword == "HAI":
            self.parse_tree = ParseNode(tok)
            self.advance()
            
            curr_node = self.parse_tree
            
            # If the next token is a variable declaration
            if self.current_tok.keyword == "WAZZUP":
                return self.wazzup(curr_node)
            elif self.current_tok.keyword == "KTHXBYE":
                curr_node.children.append(ParseNode(self.current_tok,parent=curr_node))
            else:
                raise Exception("Invalid token")
        else:
            raise Exception("Invalid token")
        
        return self.parse_tree
    
    def wazzup(self, node):
        tok = self.current_tok
        if tok.keyword == "WAZZUP":
            new_node = ParseNode(tok,parent=node)
            node.children.append(new_node)
            self.advance()
            
            # If the next token is a variable declaration
            if self.current_tok.keyword == "I HAS A":
                return self.variable_declaration(new_node)
            else:
                raise Exception("Invalid token")
            
        elif tok.keyword == "BUHBYE":
            node.next_sibling = ParseNode(tok)
            self.advance()
            
            # If the next token is a variable declaration
            if self.current_tok.keyword == "KTHXBYE":
                return self.kthxbye(node.next_sibling)
            else:
                raise Exception("Invalid token")
        else:
            raise Exception("Invalid token")
        
        return node
    
    def variable_declaration(self, node):
        tok = self.current_tok
        if tok.keyword == "I HAS A":
            new_node = ParseNode(tok,parent=node)
            node.children.append(new_node)
            self.advance()
            
            # If the next token is a variable declaration
            if self.current_tok.token_type == "Identifier":
                return self.identifier(new_node)
            else:
                raise Exception("Invalid token")
        else:
            raise Exception("Invalid token")
        
        return node
    
    def i_has_a(self, node):
        tok = self.current_tok
        if tok.keyword == "I HAS A":
            new_node = ParseNode(tok,parent=node)
            node.children.append(new_node)
            self.advance()
            
            # If the next token is a variable declaration
            if self.current_tok.token_type == "Identifier":
                return self.identifier(new_node)
            else:
                raise Exception("Invalid token")
        else:
            raise Exception("Invalid token")
        
        return node
    
    
    def identifier(self, node):
        tok = self.current_tok
        if tok.token_type == "Identifier":
            new_node = ParseNode(tok,parent=node)
            node.children.append(new_node)
            self.advance()
            
            # If the next token is a variable declaration
            if self.current_tok.keyword == "ITZ":
                return self.itz(new_node)
            else:
                raise Exception("Invalid token")
        else:
            raise Exception("Invalid token")
        
        return node
    
    def itz(self, node):
        tok = self.current_tok
        if tok.keyword == "ITZ":
            new_node = ParseNode(tok,parent=node)
            node.children.append(new_node)
            self.advance()
            
            # If the next token is a variable declaration
            if self.current_tok.token_type in ["YARN Literal", "NUMBR Literal", "NUMBAR Literal", "TROOF Literal", "TYPE Literal"]:
                return self.literal(new_node)
            else:
                raise Exception("Invalid token")
        else:
            raise Exception("Invalid token")
        
        return node
    
    def literal(self, node):
        tok = self.current_tok
        if tok.token_type in ["YARN Literal", "NUMBR Literal", "NUMBAR Literal", "TROOF Literal", "TYPE Literal"]:
            new_node = ParseNode(tok,parent=node)
            node.children.append(new_node)
            self.advance()
            # Check if the next token is another I HAS A or BUHBYE
            if self.current_tok.keyword == "I HAS A":
                return self.i_has_a(node.next_sibling)
            elif self.current_tok.keyword == "KTHXBYE":
                return self.kthxbye(node.next_sibling)
            else:
                raise Exception("Invalid token")
        else:
            raise Exception("Invalid token")
        
        return node
    
    def kthxbye(self, node):
        tok = self.current_tok
        if tok.keyword == "KTHXBYE":
            # return the tree
            node.next_sibling = ParseNode(tok)
            return node
    
        
    
    
    
if __name__ == "__main__":
    p = Parser(lexemes)
    p.program()
    print_tree(p.parse_tree)


