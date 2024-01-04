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
        # List all valid variable names
        valid_names = list(self.variables.keys())
        
        # Check if name is in the list of valid names
        if name in valid_names:
            return self.variables[name]
        else:
            # If name is not in the list of valid names, check if it is a function
            if name in self.functions:
                return self.functions[name]
            else:
                # If name is not in the list of valid names and is not a function, check if it is a keyword
                if name == "IT":
                    return self.variables[name]
                else:
                    # If name is not in the list of valid names, is not a function, and is not a keyword, raise an error
                    raise Exception("Error: Variable '" + name + "' is not defined in this scope")
    
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
                symbol_table += "\t| " + key + " | " + str(value) + " | " + str(type(value)) + " |\n"
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
            elif child_type == "<expression>":
                return self.interpret_ExpressionNode(child)
    
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
            self.interpret_AssignmentNode(statement_node)
        elif statement_node.data == "<switch>":
            self.interpret_SwitchCaseNode(statement_node)
        elif statement_node.data == "<loop>":
            # TODO: self.interpret_LoopNode(statement_node)
            pass
        elif statement_node.data == "<if-then>":
            self.interpret_IfThenNode(statement_node)
            # TODO: self.interpret_IfThenNode(statement_node)
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


    def interpret_SwitchCaseNode(self, node: ParseNode):
        it_value = self.symbolTable.get_variable("IT")
        print(f"HI: {node.children[0].data}")
        cases = node.children[1].children
        default_case = None
        cases_list = {}
        for case in cases:
            if case.data == "<case>":
                case_key = self.interpret_LiteralNode(case.children[1])
                case_body = case.children[2]
                cases_list[case_key] = case_body
            elif case.data == "<default>":  
                default_case= case.children[1]
        if it_value in cases_list:
            gtfo_flag = self.interpret_StatementsNode(cases_list[it_value])        
        
        if gtfo_flag:
            return
        self.interpret_StatementsNode(default_case)
                       

    def interpret_IfThenNode(self, node: ParseNode):
        # expression_value = self.interpret_ExpressionNode(node.children[0])
        # self.symbolTable.add_variable("IT", expression_value)
        # if_clause = node.children[2]
        # else_clause = node.children[3]
        # if expression_value:
        #     self.interpret_StatementsNode(if_clause.children[1])
        # else:
        #     self.interpret_StatementsNode(else_clause.children[1])
        expression_value = self.interpret_ExpressionNode(node.children[0])
        self.symbolTable.add_variable("IT", expression_value)
        if_clause = node.children[2]
        elif_clauses = [node.children[i] for i in range(3, len(node.children) - 2)]
        else_clause = node.children[-2]
        noMatch = True
        # if expression is true, execute statements
        if expression_value:
            self.interpret_StatementsNode(if_clause.children[1])
        # if expression is false, check elif clauses
        else:
            for elif_clause in elif_clauses:
                # if expression is true, execute statements and break
                if self.interpret_ExpressionNode(elif_clause.children[1]):
                    self.interpret_StatementsNode(elif_clause.children[2])
                    noMatch = False
                    break
            # if no elif clause is true, execute else clause
            if noMatch:
                self.interpret_StatementsNode(else_clause.children[1])
        
                
    
    def interpret_StatementsNode(self, node: ParseNode):
        for child in node.children:
            if child.children[0].data == "GTFO":
                return True
            self.interpret_StatementNode(child)
    
    def interpret_AssignmentNode(self, node: ParseNode):
        symbol_name = node.children[0].data
        symbol_value = self.interpret_ValueNode(node.children[2])
        # Get the value in the symbol table to check if it exists
        if self.symbolTable.get_variable(symbol_name) != None:
            self.symbolTable.add_variable(symbol_name, symbol_value)
        else:
            raise Exception("Error: Variable '" + symbol_name + "' is not defined in this scope")
            

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
            
    def backtracking(self, node: ParseNode, data: str):
        # Find the first parent node with the given data or return None
        while node.data != data:
            node = node.parent
            if node == None:
                return None
        return node
    
        
    def interpret_ExpressionNode(self, node: ParseNode):
        expression_node = node.children[0] 

        if expression_node.data == "<arithmetic>":   
            value = self.interpret_ArithmeticNode(expression_node)
            # Store to IT
            checkAssignment = self.backtracking(expression_node, "<assignment>")
            checkDeclar = self.backtracking(expression_node, "<declaration>")
            if checkAssignment == None:
                self.symbolTable.add_variable("IT", value)
            return value
        elif expression_node.data == "<concatenation>":
            value = self.interpret_ConcatenationNode(expression_node)
            # Store to IT
            self.symbolTable.add_variable("IT", value)
            return value
        elif expression_node.data == "<boolean>":
            value = self.interpret_BooleanNode(expression_node)
            # Store to IT
            self.symbolTable.add_variable("IT", value)
            return value
        elif expression_node.data == "<comparison>":
            value = self.interpret_ComparisonNode(expression_node)
            # Store to IT
            self.symbolTable.add_variable("IT", value)
            return value
        elif expression_node.data == "<typecasting>":
            value = self.interpret_TypecastingNode(expression_node)
            self.symbolTable.add_variable("IT", value)
            return value
        elif expression_node.data == "<recasting>":
            value = self.interpret_RecastingNode(expression_node)
            return value
        elif expression_node.data == "<function_call>":
            # TODO: self.interpret_FunctionCallNode(expression_node)
            pass
        else:
            # TODO: raise error
            pass
    
    # ==== ARITHMETIC operations ====
    # type checking (must be NUMBR or NUMBAR)
    def arithmetic_value_check(self, value):
        # if not NUMBR OR NUMBAR, explicitly cast to NUMBR OR NUMBAR
        # if cannot be caster to NUMBR OR NUMBAR, raise error
        if (type(value) == str):
            try:
                # TODO: determine if should be typecasted to int or float (currently FLOAT always)
                value = float(value)
            except:
                raise Exception(f"Typecast Error: '{value}' cannot be casted to NUMBR or NUMBAR")
        return value
    

    def interpret_ArithmeticNode(self, node: ParseNode):
        # children value can be a constant, an identifier, or another arithmetic expression
        operator = node.children[0].data
        left = node.children[1]     # <value>
        right = node.children[3]    # <value>
        
        left_type = left.children[0].data   # <literal> or <identifier> or <expression>
        right_type = right.children[0].data # <literal> or <identifier> or <expression>

        # get value of left and right
        # if left_type == "<expression>":
        #     left_value = self.interpret_ArithmeticNode(left.children[0].children[0])
        # elif left_type != "<expression>":
        #     left_value = self.interpret_ValueNode(left)
        # if right_type == "<expression>":
        #     right_value = self.interpret_ArithmeticNode(right.children[0].children[0])
        # elif right_type != "<expression>":
        #     right_value = self.interpret_ValueNode(right)
        left_value = self.interpret_ValueNode(left)
        right_value = self.interpret_ValueNode(right)

        
        # check type and implicitly cast if necessary
        left_value = self.arithmetic_value_check(left_value)
        right_value = self.arithmetic_value_check(right_value)

        # type should be <literal> or <identifier> at this point
        print(operator)
        if operator == "SUM OF":
            print(left_value + right_value)
            return left_value + right_value
        elif operator == "DIFF OF":
            print(left_value - right_value)
            return left_value - right_value
        elif operator == "PRODUKT OF":
            print(left_value * right_value)
            return left_value * right_value
        elif operator == "QUOSHUNT OF":
            # Division by zero error    
            if right_value == 0:
                raise Exception("Division by Zero Error: Cannot divide by zero")
            print(left_value / right_value)
            return left_value / right_value
        elif operator == "MOD OF":
            print(left_value % right_value)
            return left_value % right_value
        elif operator == "BIGGR OF":
            print(max(left_value, right_value))
            return max(left_value, right_value)
        elif operator == "SMALLR OF":
            print(min(left_value, right_value))
            return min(left_value, right_value)
    # ==== END ARITHMETIC operations ====
    
    # ==== CONCATENATION operations ====
    def interpret_ConcatenationNode(self, node: ParseNode):
        # array of strings to be concatenated
        strings = []

        # children value can be of any data type but will be typecast to yarns
        for children in node.children:
            if children.data == "<value>":
                value = str(self.interpret_ValueNode(children))
                # TROOF interepted literals are WIN or FAIL
                if value == "True":
                    value = "WIN"
                elif value == "False":
                    value = "FAIL"

                strings.append(value)

        value = ''.join(strings)

        print(value)
        return value    
    # ==== END CONCATENATION operations ====

    # ==== BOOLEAN operations ====
    # type checking (must be TROOF)
    def boolean_value_check(self, value):
        false_values = [0, 0.0, "", None, "FAIL"]
        if value not in false_values:
            value = True
        else:
            value = False
        return value

    def interpret_BooleanNode(self, node: ParseNode):
        # children value can be of any data type but will be typecast to TROOF
        # array of strings to be concatenated
        print(node.data)
        operator = node.children[0].data

        print(operator)
        # finite; two operands
        if operator != "ALL OF" and operator != "ANY OF" and operator != "NOT":
            left_value = self.interpret_ValueNode(node.children[1])     # <value>
            right_value = self.interpret_ValueNode(node.children[3])    # <value>
            print(left_value, right_value) 

            # check type and implicitly cast if necessary (must be TROOF)
            left_value = self.boolean_value_check(left_value)
            right_value = self.boolean_value_check(right_value)

            if operator == "BOTH OF":       # AND
                print(operator, left_value and right_value)
                return (left_value and right_value)
            elif operator == "EITHER OF":   # OR
                print(operator, (left_value or right_value))
                return (left_value or right_value)
            elif operator == "WON OF":      # XOR
                print(operator, (left_value ^ right_value))
                return (left_value ^ right_value)
        # finite; one operand
        elif operator == "NOT":
            only_value = self.interpret_ValueNode(node.children[1])
            # check type and implicitly cast if necessary (must be TROOF)
            only_value = self.boolean_value_check(only_value)
            print(operator, (not only_value))
            return (not only_value)
        # infinite
        else:
            values = []
            for children in node.children:
                if children.data == "<value>":
                    value = self.interpret_ValueNode(children)
                    # check type and implicitly cast if necessary (must be TROOF)
                    value = self.boolean_value_check(value)
                    values.append(value)
            
            if operator == "ALL OF":    # infinite arity AND
                print(operator, all(values))
                return all(values)
            elif operator == "ANY OF":  # infinite arity OR
                print(operator, any(values))
                return any(values)
    # ==== END BOOLEAN operations ====
            

    # ==== COMPARISON operations ====
    def interpret_ComparisonNode(self, node: ParseNode):
        # NUMBR or NUMBAR only

        # comparison operations
        if len(node.children) == 4:
            print(">>> comparison operations")
            operator = node.children[0].data
            left_value = self.interpret_ValueNode(node.children[1])
            right_value = self.interpret_ValueNode(node.children[3])

            # check type (no automatic typecasting)
            if type(left_value) != int and type(left_value) != float:
                raise Exception(f"Type Error: '{left_value}' is not a NUMBR or NUMBAR")
            if type(right_value) != int and type(right_value) != float:
                raise Exception(f"Type Error: '{right_value}' is not a NUMBR or NUMBAR")

            if operator == "BOTH SAEM":
                print(operator, (left_value == right_value))
                return (left_value == right_value)
            elif operator == "DIFFRINT":
                print(operator, (left_value != right_value))
                return (left_value != right_value)
        # relational operations
        else :
            print(">>> relational operations")
            operator = node.children[0].data
            operator2 = node.children[3].data
            left_value = self.interpret_ValueNode(node.children[1])
            left_value2 = self.interpret_ValueNode(node.children[4])
            right_value = self.interpret_ValueNode(node.children[6])

            # check type (no automatic typecasting)
            if type(left_value) != int and type(left_value) != float:
                raise Exception(f"Type Error: '{left_value}' is not a NUMBR or NUMBAR")
            if type(right_value) != int and type(right_value) != float:
                raise Exception(f"Type Error: '{right_value}' is not a NUMBR or NUMBAR")
            # left_value should have the same value as left_value2
            if left_value != left_value2:
                raise Exception(f"Type Error: '{left_value}' is not equal to '{left_value2}'")
            
            if operator == "BOTH SAEM":
                if operator2 == "BIGGR OF":
                    print(operator, (left_value >= right_value))
                    return (left_value >= right_value)
                elif operator2 == "SMALLR OF":
                    print(operator, (left_value <= right_value))
                    return (left_value <= right_value)
            elif operator == "DIFFRINT":
                if operator2 == "BIGGR OF":
                    print(operator, (left_value < right_value))
                    return (left_value < right_value)
                elif operator2 == "SMALLR OF":
                    print(operator, (left_value > right_value))
                    return (left_value > right_value)
    # ==== END COMPARISON operations ====
                

    # ==== TYPECASTING operations ====
    def interpret_TypecastingNode(self, node: ParseNode):
        # NOOB 
            # NOOBs can be implicitly typecast into TROOF (implicit typecasting to any other types will result in an error)
            # Explicit typecasting of NOOBs is allowed and will result to zero/empty values
        # TROOF
            # Empty string ("") and numerical zero -- cast to  FAIL
            # All other values, except those mentioned above are cast to WIN
            # Casting WIN to numeric -- 1 or 1.0s
            # Casting FAIL to numberic -- 0
        # NUMBAR
            # Casting NUMBAR to NUMBR -- truncate the decimal point of the NUMBAR
            # Casting NUMBAR to YARN -- will truncate the decimal portion up to two decimal places
        # NUMBR
            # Casting NUMBR to NUMBAR -- convert value into floating point. (value should be retained)
            # Casting NUMBR to YARN -- convert the value into a string of characters
        # YARN 
            # YARN can be successfully cast into a NUMBAR or NUMBR if YARN does not contain non-numerical, non-hyphen, nom-period characters
        
        print(node.data)
        
        # using MAEK operator only modifies the resulting value and not the variable involved
        if node.children[0].data == "MAEK":
            only_value = self.interpret_ValueNode(node.children[1])
            # syntax may be: (1) MAEK var1 A NUMBAR or (2) MAEK var1 A NUMBR
            if node.children[2].data == "A":
                typecast_type = node.children[3].data
            else:
                typecast_type = node.children[2].data

            if typecast_type == "NOOB":
                raise Exception(f"Typecast Error: '{only_value}' cannot be casted to NOOB")
            elif typecast_type == "TROOF":
                if not only_value:
                    print("FAIL")
                    return False
                else:
                    print("WIN")
                    return True
            elif typecast_type == "NUMBAR":
                try:
                    if only_value == None:
                        return 0.0
                    else:
                        print(float(only_value))
                        return float(only_value)
                except:
                    raise Exception(f"Typecast Error: '{only_value}' cannot be casted to NUMBAR")
            elif typecast_type == "NUMBR":
                try:
                    if only_value == None:
                        return 0
                    else:
                        print(int(only_value))
                        return int(only_value)
                except:
                    raise Exception(f"Typecast Error: '{only_value}' cannot be casted to NUMBR")
            elif typecast_type == "YARN":
                if only_value == None:
                    return ""
                elif type(only_value) == str:
                    print(str(only_value))
                    return str(only_value)
                elif type(only_value) == int or type(only_value) == float:
                    print(str(round(only_value, 2)))
                    return str(round(only_value, 2))
                elif type(only_value) == bool:
                    if only_value:
                        print("WIN")
                        return "WIN"
                    else:
                        print("FAIL")
                        return "FAIL"

                




    def interpret_RecastingNode(self, node: ParseNode):
        # NOOB 
            # NOOBs can be implicitly typecast into TROOF (implicit typecasting to any other types will result in an error)
            # Explicit typecasting of NOOBs is allowed and will result to zero/empty values
        # TROOF
            # Empty string ("") and numerical zero -- cast to  FAIL
            # All other values, except those mentioned above are cast to WIN
            # Casting WIN to numeric -- 1 or 1.0s
            # Casting FAIL to numberic -- 0
        # NUMBAR
            # Casting NUMBAR to NUMBR -- truncate the decimal point of the NUMBAR
            # Casting NUMBAR to YARN -- will truncate the decimal portion up to two decimal places
        # NUMBR
            # Casting NUMBR to NUMBAR -- convert value into floating point. (value should be retained)
            # Casting NUMBR to YARN -- convert the value into a string of characters
        # YARN 
            # YARN can be successfully cast into a NUMBAR or NUMBR if YARN does not contain non-numerical, non-hyphen, nom-period characters
        
        print(node.data)
        
        # using MAEK operator only modifies the resulting value and not the variable involved
        print(node.children[1].data)
        if node.children[1].data == "IS NOW A":
            variable_name = node.children[0].children[0].children[0].data
            
            only_value = self.interpret_ValueNode(node.children[0])
            print(f"ONLY VALUE: {only_value}")
            # syntax may be: number IS NOW A NUMBAR BTW number is NUMBAR type now (17.0)
            typecast_type = node.children[2].data
            
            if typecast_type == "NOOB":
                raise Exception(f"Recasting Error: '{only_value}' cannot be casted to NOOB")
            elif typecast_type == "TROOF":
                if not only_value:
                    print("FAIL")
                    self.symbolTable.add_variable(variable_name, False)
                    return self.symbolTable.get_variable(variable_name)
                else:
                    self.symbolTable.add_variable(variable_name, True)
                    print("WIN")
                    return self.symbolTable.get_variable(variable_name)
            elif typecast_type == "NUMBAR":
                try:
                    if only_value == None:
                        self.symbolTable.add_variable(variable_name, 0.0)
                        return self.symbolTable.get_variable(variable_name)
                    else:
                        self.symbolTable.add_variable(variable_name, float(only_value))
                        return self.symbolTable.get_variable(variable_name)
                except:
                    raise Exception(f"Recasting Error: '{only_value}' cannot be casted to NUMBAR")
            elif typecast_type == "NUMBR":
                try:
                    if only_value == None:
                        self.symbolTable.add_variable(variable_name, 0)
                        return self.symbolTable.get_variable(variable_name)
                    else:
                        print(f"NUMBR: {only_value}")
                        self.symbolTable.add_variable(variable_name, int(only_value))
                        return self.symbolTable.get_variable(variable_name)
                except:
                    raise Exception(f"Recasting Error: '{only_value}' cannot be casted to NUMBR")
            elif typecast_type == "YARN":
                if only_value == None:
                    self.symbolTable.add_variable(variable_name, "")
                    return self.symbolTable.get_variable(variable_name)
                
                # If decimal (NUMBAR) round to 2 decimal places
                if type(only_value) == float:
                    only_value = round(only_value, 2)
                
                if type(only_value) == bool:
                    if only_value:
                        only_value = "WIN"
                    else:
                        only_value = "FAIL"
                        
                self.symbolTable.add_variable(variable_name, str(only_value))
                return self.symbolTable.get_variable(variable_name)
    
    # ==== END TYPECASTING operations ====
    
    

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
    