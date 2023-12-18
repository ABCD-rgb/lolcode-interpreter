from syntax_analyzer import Parser, ParseNode, print_tree
from lexer import lexer


class SymbolTable:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.call_stack = []
        self.loop_stack = []
        self.return_stack = []
        self.current_function = None
        
    def add_variable(self, name, value):
        self.variables[name] = value
        
    def get_variable(self, name):
        try:
            to_ret = self.variables[name]
        except KeyError:
            print("Variable " + name + " not found")
            to_ret = None
        
        return to_ret
    
    def add_function(self, name, value):
        self.functions[name] = value
        
    def get_function(self, name):
        return self.functions[name]
    
    def push_call_stack(self, value):
        self.call_stack.append(value)
        
    def pop_call_stack(self):
        return self.call_stack.pop()
    
    def push_loop_stack(self, value):
        self.loop_stack.append(value)
        
    def pop_loop_stack(self):
        return self.loop_stack.pop()
    
    def push_return_stack(self, value):
        self.return_stack.append(value)
        
    def pop_return_stack(self):
        return self.return_stack.pop()
    
    def set_current_function(self, value):
        self.current_function = value
        
    def get_current_function(self):
        return self.current_function
    
    def print_symbol_table(self):
        symbol_table = ""
        symbol_table += "=== SYMBOL TABLE ===\n"

        symbol_table += "Variables: \n"
        if len(self.variables) == 0:
            symbol_table += "\tEMPTY\n"
        else:
            for key, value in self.variables.items():
                symbol_table += "\t| " + key + " | " + str(value) + " |\n"
        symbol_table += "Functions: \n"
        if len(self.functions) == 0:
            symbol_table += "\tEMPTY\n"
        else:
            for key, value in self.functions.items():
                symbol_table += "\t| " + key + " | " + str(value) + " |\n"
        symbol_table += "Call Stack: \n"
        if len(self.call_stack) == 0:
            symbol_table += "\tEMPTY\n"
        else:
            for value in self.call_stack:
                symbol_table += "\t| " + str(value) + " |\n"
        symbol_table += "Loop Stack: \n"
        if len(self.loop_stack) == 0:
            symbol_table += "\tEMPTY\n"
        else:
            for value in self.loop_stack:
                symbol_table += "\t| " + str(value) + " |\n"
        symbol_table += "Return Stack: \n"
        if len(self.return_stack) == 0:
            symbol_table += "\tEMPTY\n"
        else:
            for value in self.return_stack:
                symbol_table += "\t| " + str(value) + " |\n"
        symbol_table += "Current Function: \n"
        if self.current_function == None:
            symbol_table += "\tEMPTY\n"
        else:
            symbol_table += "\t| " + str(self.current_function) + " |\n"
        symbol_table += "====================\n"
        print(symbol_table)
    
    def __str__(self):
        return "SymbolTable: " + str(self.variables) + ", " + str(self.functions) + ", " + str(self.call_stack) + ", " + str(self.loop_stack) + ", " + str(self.return_stack) + ", " + str(self.current_function)
    
    def __repr__(self):
        return self.__str__()

class Interpreter:
    def __init__(self, tree: ParseNode, symbols: SymbolTable):
        self.tree = tree
        self.symbolTable = symbols
        
    def interpret(self):
        self.interpret_root(self.tree)
        
    def interpret_root(self, node: ParseNode):
        if node.data == "<program>":
            for child in node.children:
                self.interpret_ProgramNode(child)
                
    
    def interpret_ProgramNode(self, node: ParseNode):
        if node.data == "HAI":
            print("HAI")
        elif node.data == "KTHXBYE":
            print("KTHXBYE")
        elif node.data == "<wazzup>":
            for node in node.children:
                self.interpret_WazzupNode(node)
        elif node.data == "<statements>":
            for node in node.children:
                self.interpret_StatementNode(node)
            pass
        elif node.data == "<function>":
            pass
        else:
            raise Exception("Unknown node: " + node.data)
        
    
    def interpret_WazzupNode(self, node: ParseNode):
        if node.data == "WAZZUP":
            pass
        elif node.data == "<declarations>":
            for node in node.children:
                self.interpret_DeclarationsNode(node)
        elif node.data == "BUHBYE":
            pass
        
    
    def interpret_DeclarationsNode(self, node: ParseNode):
        symbol_name = node.children[1].data
        # Check if symbol_name is in the symbol table already, raise error if it is
        if symbol_name in self.symbolTable.variables:
            raise Exception("Error: Variable '" + symbol_name + "' is already defined in this scope") 
        
        if len(node.children) == 4:
            symbol_value = self.interpret_ValueNode(node.children[3])
        else:
            symbol_value = None
        
        self.symbolTable.add_variable(symbol_name, symbol_value)
            
        

    
    def interpret_ValueNode(self, node: ParseNode):
        for child in node.children:
            child_type = child.data
            if child_type == "<literal>":
                # print("CHILD DATA: " + child.data)
                return self.interpret_LiteralNode(child)
            elif child_type == "<identifier>":
                return self.interpret_IdentifierNode(child)
    
        return node.data
    
    def interpret_IdentifierNode(self, node: ParseNode):
        # print("IDENTIFIER NODE: " + node.children[0].data)
        symbol_name = node.children[0].data
        return self.symbolTable.get_variable(symbol_name)
    
    
    def interpret_LiteralNode(self, node: ParseNode):
        data_node = node.children[0]
        if data_node.data == "<NUMBR>":
            return int(data_node.children[0].data)
        elif data_node.data == "<NUMBAR>":
            return float(data_node.children[0].data)
        elif data_node.data == "<STRING>":
            return data_node.children[1].data
        elif data_node.data == "<TROOF>":
            return data_node.children[0].data == "WIN"
        
    def interpret_StatementNode(self, node: ParseNode):
        statement_node = node.children[0]
        
        if statement_node.data == "<input>":
            self.interpret_InputNode(statement_node)
        elif statement_node.data == "<output>":
            self.interpret_OutputNode(statement_node)
        elif statement_node.data == "<expression>":
            self.interpret_ExpressionNode(statement_node)
        elif statement_node.data == "<assignment>":
            # TODO: self.interpret_AssignmentNode(statement_node)
            pass
        elif statement_node.data == "<switch>":
            # TODO: self.interpret_SwitchNode(statement_node)
            pass
        elif statement_node.data == "<loop>":
            # TODO: self.interpret_LoopNode(statement_node)
            pass
        elif statement_node.data == "<function>":
            # TODO: self.interpret_FunctionNode(statement_node)
            pass
        elif statement_node.data == "<function call>":
            # TODO: self.interpret_FunctionCallNode(statement_node)
            pass
        else:
            # TODO: raise error
            pass
            

    def interpret_InputNode(self, node: ParseNode):
        symbol_name = node.children[1].data
        symbol_value = input()
        self.symbolTable.add_variable(symbol_name, symbol_value)
        
    def interpret_OutputNode(self, node: ParseNode):
        
        operands = []
        newLine = True
        
        for child in node.children:
            # Each operand is seperated by a + sign
            # Each operand is a <value> node
            if child.data == "<value>":
                operands.append(self.interpret_ValueNode(child))
            if child.data == "!":
                newLine = False
                
        # Print each operand and if newLine is true, print a new line else don't
        for operand in operands:
            print(operand, end = "")
        if newLine:
            print()
            

    def interpret_ExpressionNode(self, node: ParseNode):
        expression_node = node.children[0] 

        if expression_node.data == "<arithmetic>":   
            self.interpret_ArithmeticNode(expression_node)
            pass
        elif expression_node.data == "<concatenation>":
            # TODO: self.interpret_ConcatenationNode(expression_node)
            pass
        elif expression_node.data == "<boolean>":
            # TODO: self.interpret_BooleanNode(expression_node)
            pass
        elif expression_node.data == "<comparison>":
            # TODO: self.interpret_ComparisonNode(expression_node)
            pass
        elif expression_node.data == "<typecasting>":
            # TODO: self.interpret_TypecastingNode(expression_node)
            pass
        elif expression_node.data == "<recasting>":
            # TODO: self.interpret_RecastingNode(expression_node)
            pass
        elif expression_node.data == "<function_call>":
            # TODO: self.interpret_FunctionCallNode(expression_node)
            pass
        else:
            # TODO: raise error
            pass
    
    # ==== ARITHMETIC operations ====
    def interpret_ArithmeticNode(self, node: ParseNode):
        for child in node.children:
            print(child.data)
    # ==== END ARITHMETIC operations ====
                
    
    
    
        
        
        
def main():
    symbols = SymbolTable()
    symbols.add_variable("IT", None)
    lexemes = lexer("test.lol")
    parser = Parser(lexemes)
    tree = parser.parse()
    interpreter = Interpreter(tree, symbols)
    interpreter.interpret()
    # print(symbols)
    symbols.print_symbol_table()
    
if __name__ == '__main__':
    main()
    