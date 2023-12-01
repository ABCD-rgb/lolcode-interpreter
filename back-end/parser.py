import patterns as p
import lexer as l


lexemes = l.lexer("parser_test.lol")
# print(lexemes)

class ParseNode:
    def __init__(self, data, parent=None):
        self.parent = parent
        self.data = data
        self.children = []

    def __str__(self):
        tree = self.data + '\n'
        for child in self.children:
            tree += child.__str__()
        return tree

def print_tree(node, indent=0, prefix=''):
    if node is not None:
        print(' ' * indent + prefix + node.data)
        for child in node.children:
            print_tree(child, indent + 4, "|-- ")


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
        # If the token is HAI then we can continue
        self.parse_tree = ParseNode("<program>")
        
        if self.current_tok.keyword == "HAI":
            self.parse_tree.children.append(ParseNode(self.current_tok.keyword, parent=self.parse_tree))
            self.advance()
            
        if self.current_tok.keyword == "WAZZUP":
            self.wazzup(self.parse_tree)
            
        if self.current_tok.keyword != "WAZZUP":
            self.statements(self.parse_tree)
    
        if self.current_tok.keyword == "KTHXBYE":
            self.parse_tree.children.append(ParseNode(self.current_tok.keyword, parent=self.parse_tree))
            return self.parse_tree
        
        raise Exception(f"Syntax Error: Invalid token: {self.current_tok.keyword}")
        
    def wazzup(self, node):
        wazzup_node = ParseNode("<wazzup>", parent=node)
        
        if self.current_tok.keyword == "WAZZUP":
            node.children.append(wazzup_node)
            wazzup_node.children.append(ParseNode(self.current_tok.keyword, parent=wazzup_node))
            self.advance()
        
        if self.current_tok.keyword == "I HAS A":
            self.declarations(wazzup_node)
            
        if self.current_tok.keyword == "BUHBYE":
            wazzup_node.children.append(ParseNode(self.current_tok.keyword, parent=wazzup_node))
            self.advance()
            return

        raise Exception(f"Syntax Error: Invalid token: {self.current_tok.keyword}")


    def declarations(self, node):
        declarations_node = ParseNode("<declarations>", parent=node)
        
        if self.current_tok.keyword  == "I HAS A":
            node.children.append(declarations_node)
            self.declaration(declarations_node)
        
        return


    def declaration(self, node):
        declaration_node = ParseNode("<declaration>", parent=node)

        if self.current_tok.keyword == "I HAS A":
            node.children.append(declaration_node)
            declaration_node.children.append(ParseNode(self.current_tok.keyword, parent=declaration_node))
            self.advance()
            
            if self.current_tok.token_type == "Identifier":
                declaration_node.children.append(ParseNode(self.current_tok.keyword, parent=declaration_node))
                self.advance()
                
                if self.current_tok.keyword == "ITZ":
                    declaration_node.children.append(ParseNode(self.current_tok.keyword, parent=declaration_node))
                    self.advance()
                    self.value(declaration_node)

                
                if self.current_tok.keyword == "I HAS A":
                    self.declaration(node)
                
            else:
                raise Exception(f"Syntax Error: Invalid token: {self.current_tok.keyword}")
    
    def statements(self, node):
        statements_node = ParseNode("<statements>", parent=node)
        
        if self.current_tok.keyword != "KTHXBYE":
            if self.current_tok.keyword in ["OMG", "OMGWTF", "OIC"]:
                return
            node.children.append(statements_node)
            self.statement(statements_node)
        else:
            return
        
    
    def statement(self, node):
            try:
                while self.current_tok.keyword != "KTHXBYE":
                    statement_node = ParseNode("<statement>", parent=node)
                    if self.current_tok.token_type == "Identifier":
                        node.children.append(statement_node)
                        self.assignment(statement_node)
                    elif self.current_tok.keyword == "GIMMEH":
                        node.children.append(statement_node)
                        self.input(statement_node)
                    elif self.current_tok.keyword == "VISIBLE":
                        node.children.append(statement_node)
                        self.output(statement_node)
                    elif self.current_tok.keyword == "WTF?":
                        node.children.append(statement_node)
                        self.switch(statement_node)
                    elif node.parent.parent.parent.data == "<switch>":
                        if self.current_tok.keyword == "OMGWTF":
                            return
                        elif self.current_tok.keyword == "OMG":
                            return
                        elif self.current_tok.keyword == "OIC":
                            return
                        elif self.current_tok.keyword == "GTFO":
                            node.children.append(statement_node)
                            statement_node.children.append(ParseNode(self.current_tok.keyword, parent=statement_node))
                            self.advance()
                    # elif self.current_tok.keyword == "IM IN YR":
                    #     node.children.append(statement_node)
                    #     self.loop(statement_node)
                    # elif self.current_tok.keyword == "I IZ":
                    #     node.children.append(statement_node)
                    #     self.function_call(statement_node)
                    else:
                        raise Exception(f"Syntax Error: Invalid token: {self.current_tok.keyword}: {self.current_tok.token_type}")
            except AttributeError:
                raise Exception(f"Syntax Error: Invalid token: {self.current_tok.keyword}: {self.current_tok.token_type}")
                    
            return
    

    # def function_call(self, node):
    #     function_call_node = ParseNode("<function_call>", parent=node)
    #     if self.current_tok.keyword == "I IZ":
    #         node.children.append(function_call_node)
    #         function_call_node.children.append(ParseNode(self.current_tok.keyword, parent=function_call_node))
    #         self.advance()
    #         if self.current_tok.token_type == "Identifier":
    #             function_call_node.children.append(ParseNode(self.current_tok.keyword, parent=function_call_node))
    #             self.advance()
    #         else:
    #             raise Exception(f"Syntax Error: Invalid token: {self.current_tok.keyword}: {self.current_tok.token_type}")
    #     else:
    #         raise Exception(f"Syntax Error: Invalid token: {self.current_tok.keyword}: {self.current_tok.token_type}")

    def switch(self, node):
        switch_node = ParseNode("<switch>", parent=node)
        if self.current_tok.keyword == "WTF?":
            node.children.append(switch_node)
            switch_node.children.append(ParseNode(self.current_tok.keyword, parent=switch_node))
            self.advance()
            self.cases(switch_node)
            if self.current_tok.keyword == "OIC":
                switch_node.children.append(ParseNode(self.current_tok.keyword, parent=switch_node))
                self.advance()
        else:
            raise Exception(f"Syntax Error: Invalid token: {self.current_tok.keyword}: {self.current_tok.token_type}")
    
    def cases(self, node):
        cases_node = ParseNode("<cases>", parent=node)
        
        # If the current token is OMG
        if self.current_tok.keyword == "OMG":
            # Append the cases node to the parent node
            node.children.append(cases_node)
            pass
        
        while self.current_tok.keyword == "OMG":
            self.case(cases_node)
            
        if self.current_tok.keyword == "OMGWTF":
            self.default(cases_node)
            
        if self.current_tok.keyword == "OIC":
            return
        
        raise Exception(f"Syntax Error: Invalid token: {self.current_tok.keyword}: {self.current_tok.token_type}")
    
    def case(self, node):
        case_node = ParseNode("<case>", parent=node)
        if self.current_tok.keyword == "OMG":
            node.children.append(case_node)
            case_node.children.append(ParseNode(self.current_tok.keyword, parent=case_node))
            self.advance()
            self.literal(case_node)
            self.statements(case_node)
        else:
            raise Exception(f"Syntax Error: Invalid token: {self.current_tok.keyword}: {self.current_tok.token_type}")
    
    def default(self, node):
        default_node = ParseNode("<default>", parent=node)
        if self.current_tok.keyword == "OMGWTF":
            node.children.append(default_node)
            default_node.children.append(ParseNode(self.current_tok.keyword, parent=default_node))
            self.advance()
            self.statements(default_node)
        else:
            raise Exception(f"Syntax Error: Invalid token: {self.current_tok.keyword}: {self.current_tok.token_type}")
    
    def value(self, node):
        value_node = ParseNode("<value>", parent=node)
        if self.current_tok.token_type in ["Identifier"]:
            node.children.append(value_node)
            value_node.children.append(ParseNode(self.current_tok.keyword, parent=value_node))
            self.advance()
        elif self.current_tok.token_type in ["String Delimiter", "NUMBR Literal", "NUMBAR Literal", "TROOF Literal", "TYPE Literal"]:
            node.children.append(value_node)
            self.literal(value_node)
        # === TODO: Add support for expressions
        else:
            raise Exception(f"Syntax Error: Invalid token: {self.current_tok.keyword}: {self.current_tok.token_type}")
    
    def literal(self, node):
        literal_node = ParseNode("<literal>", parent=node)
        if self.current_tok.token_type in ["NUMBR Literal", "NUMBAR Literal", "TROOF Literal", "TYPE Literal"]:
            node.children.append(literal_node)
            literal_node.children.append(ParseNode(self.current_tok.keyword, parent=literal_node))
            self.advance()
        elif self.current_tok.token_type in ["String Delimiter"]:
            node.children.append(literal_node)
            literal_node.children.append(ParseNode(self.current_tok.keyword, parent=literal_node))
            self.advance()
            literal_node.children.append(ParseNode(self.current_tok.keyword, parent=literal_node))
            self.advance()
            literal_node.children.append(ParseNode(self.current_tok.keyword, parent=literal_node))
            self.advance()
        else:
            raise Exception(f"Syntax Error: Invalid token: {self.current_tok.keyword}: {self.current_tok.token_type}")
    
    def output(self, node):
        output_node = ParseNode("<output>", parent=node)
        if self.current_tok.keyword == "VISIBLE":
            node.children.append(output_node)
            output_node.children.append(ParseNode(self.current_tok.keyword, parent=output_node))
            self.advance()
            self.value(output_node)
                # === TODO: Add support for "!"

    
    def input(self, node):
        input_node = ParseNode("<input>", parent=node)
        if self.current_tok.keyword == "GIMMEH":
            node.children.append(input_node)
            input_node.children.append(ParseNode(self.current_tok.keyword, parent=input_node))
            self.advance()
            if self.current_tok.token_type == "Identifier":
                input_node.children.append(ParseNode(self.current_tok.keyword, parent=input_node))
                self.advance()
            else:
                raise Exception(f"Syntax Error: Invalid token: {self.current_tok.keyword}: {self.current_tok.token_type}")

        return
    
    def assignment(self, node):
        assignment_node = ParseNode("<assignment>", parent=node)
        
        if self.current_tok.token_type == "Identifier":
            node.children.append(assignment_node)
            assignment_node.children.append(ParseNode(self.current_tok.keyword, parent=assignment_node))
            self.advance()
            if self.current_tok.keyword == "R":
                assignment_node.children.append(ParseNode(self.current_tok.keyword, parent=assignment_node))
                self.advance()
                self.value(assignment_node)
            else: 
                raise Exception(f"Syntax Error: Invalid token: {self.current_tok.keyword}: {self.current_tok.token_type}")

       
    #         # If the next token is a variable declaration
    #         if self.current_tok.keyword == "WAZZUP":
    #             return self.wazzup(curr_node)
    #         elif self.current_tok.keyword == "KTHXBYE":
    #             curr_node.children.append(ParseNode(self.current_tok,parent=curr_node))
    #         else:
    #             raise Exception("Invalid token")
    #     else:
    #         raise Exception("Invalid token")
        
    #     return self.parse_tree
    
    # def wazzup(self, node):
    #     tok = self.current_tok
    #     if tok.keyword == "WAZZUP":
    #         new_node = ParseNode(tok,parent=node)
    #         node.children.append(new_node)
    #         self.advance()
            
    #         # If the next token is a variable declaration
    #         if self.current_tok.keyword == "I HAS A":
    #             return self.variable_declaration(new_node)
    #         else:
    #             raise Exception("Invalid token")
            
    #     elif tok.keyword == "BUHBYE":
    #         node.next_sibling = ParseNode(tok)
    #         self.advance()
            
    #         # If the next token is a variable declaration
    #         if self.current_tok.keyword == "KTHXBYE":
    #             return self.kthxbye(node.next_sibling)
    #         else:
    #             raise Exception("Invalid token")
    #     else:
    #         raise Exception("Invalid token")
        
    #     return node
    
    # def variable_declaration(self, node):
    #     tok = self.current_tok
    #     if tok.keyword == "I HAS A":
    #         new_node = ParseNode(tok,parent=node)
    #         node.children.append(new_node)
    #         self.advance()
            
    #         # If the next token is a variable declaration
    #         if self.current_tok.token_type == "Identifier":
    #             return self.identifier(new_node)
    #         else:
    #             raise Exception("Invalid token")
    #     else:
    #         raise Exception("Invalid token")
        
    #     return node
    
    # def i_has_a(self, node):
    #     tok = self.current_tok
    #     if tok.keyword == "I HAS A":
    #         new_node = ParseNode(tok,parent=node)
    #         node.children.append(new_node)
    #         self.advance()
            
    #         # If the next token is a variable declaration
    #         if self.current_tok.token_type == "Identifier":
    #             return self.identifier(new_node)
    #         else:
    #             raise Exception("Invalid token")
    #     else:
    #         raise Exception("Invalid token")
        
    #     return node
    
    
    # def identifier(self, node):
    #     tok = self.current_tok
    #     if tok.token_type == "Identifier":
    #         new_node = ParseNode(tok,parent=node)
    #         node.children.append(new_node)
    #         self.advance()
            
    #         # If the next token is a variable declaration
    #         if self.current_tok.keyword == "ITZ":
    #             return self.itz(new_node)
    #         else:
    #             raise Exception("Invalid token")
    #     else:
    #         raise Exception("Invalid token")
        
    #     return node
    
    # def itz(self, node):
    #     tok = self.current_tok
    #     if tok.keyword == "ITZ":
    #         new_node = ParseNode(tok,parent=node)
    #         node.children.append(new_node)
    #         self.advance()
            
    #         # If the next token is a variable declaration
    #         if self.current_tok.token_type in ["YARN Literal", "NUMBR Literal", "NUMBAR Literal", "TROOF Literal", "TYPE Literal"]:
    #             return self.literal(new_node)
    #         else:
    #             raise Exception("Invalid token")
    #     else:
    #         raise Exception("Invalid token")
        
    #     return node
    
    # def literal(self, node):
    #     tok = self.current_tok
    #     if tok.token_type in ["YARN Literal", "NUMBR Literal", "NUMBAR Literal", "TROOF Literal", "TYPE Literal"]:
    #         new_node = ParseNode(tok,parent=node)
    #         node.children.append(new_node)
    #         self.advance()
    #         # Check if the next token is another I HAS A or BUHBYE
    #         if self.current_tok.keyword == "I HAS A":
    #             return self.i_has_a(node.next_sibling)
    #         elif self.current_tok.keyword == "KTHXBYE":
    #             return self.kthxbye(node.next_sibling)
    #         else:
    #             raise Exception("Invalid token")
    #     else:
    #         raise Exception("Invalid token")
        
    #     return node
    
    # def kthxbye(self, node):
    #     tok = self.current_tok
    #     if tok.keyword == "KTHXBYE":
    #         # return the tree
    #         node.next_sibling = ParseNode(tok)
    #         return node
    
        
    
    
    
if __name__ == "__main__":
    p = Parser(lexemes)
    p.parse()
    print_tree(p.parse_tree)


