import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk, simpledialog
from lexer import lexer
from interpreter import SymbolTable, Interpreter
from syntax_analyzer import Parser
import sys

class TextRedirector:
    def __init__ (self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        # Make the text widget editable
        self.text_widget.config(state="normal")

        # Insert the text
        self.text_widget.insert(tk.END, text)
        self.text_widget.see(tk.END)

        # Make the text widget read-only again
        self.text_widget.config(state="disabled")
    
    def flush(self):
        pass

class InputRedirector:
    def __init__(self, input_function):
        self.input_function = input_function

    def readline(self):
        user_input = self.input_function()
        return user_input + '\n'
    
class StderrRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        # Make the text widget editable
        self.text_widget.config(state="normal")

        # Insert the text
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)

        # Make the text widget read-only again
        self.text_widget.config(state="disabled")

    def flush(self):
        pass

class InterpreterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Interpreter GUI")
        self.file_path = ""
        self.lexemes = []
        self.symbols = SymbolTable()
        self.symbols.add_variable("IT", None)
        self.variables = {}

        # File Explorer
        self.file_explorer_button = tk.Button(root, text="Open File", command=self.open_file)
        self.file_explorer_button.grid(row=0, column=0, pady=2)

        # labels
        self.lexemes_label = tk.Label(root, text="Lexemes")
        self.lexemes_label.grid(row=0, column=1, pady=2)

        self.symbol_table_label = tk.Label(root, text="Symbol Table")
        self.symbol_table_label.grid(row=0, column=2, pady=2)

        # Text Editor
        self.text_editor = scrolledtext.ScrolledText(root, width=60, height=20)
        self.text_editor.grid(row=1, column=0, pady=2, padx=2, sticky="nsew")

        # List of Tokens
        self.lexemes_table_frame, self.lexemes_table = self.create_scrollable_table(root, headers=["Lexeme", "Classification"])
        self.lexemes_table_frame.grid(row=1, column=1, pady=2, padx=2, sticky="nsew")

        # Symbol Table
        self.symbol_table_frame, self.symbol_table = self.create_scrollable_table(root, headers=["Identifier", "Value"])
        self.symbol_table_frame.grid(row=1, column=2, pady=2, padx=2, sticky="nsew")

        # Execute Button
        self.execute_button = tk.Button(root, text="Execute", command=self.execute_code)
        self.execute_button.grid(row=2, column=1, pady=2)

        # View parse tree button
        self.view_tree_button = tk.Button(root, text="View Parse Tree", command=self.view_parse_tree)
        self.view_tree_button.grid(row=2, column=2, pady=2)

        # Console
        self.console = scrolledtext.ScrolledText(root, width=80, height=20)
        self.console.config(state="disabled")
        self.console.grid(row=3, column=0, columnspan=3, pady=2, padx=5, sticky="ew")

        # Redirect the print statements to the text widget
        sys.stdout = TextRedirector(self.console)

        # Redirect the input to the input dialog
        sys.stdin = InputRedirector(self.get_input_from_dialog)

        # Redirect stderr to the text widget
        sys.stderr = StderrRedirector(self.console)

        # Configure row and column weights for resizing
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(2, weight=1)
        root.grid_rowconfigure(3, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)

        # To restore stdin on application exit
        root.protocol("WM_DELETE_WINDOW", self.restore_stdin)

    # get input from dialog box
    def get_input_from_dialog(self):
        user_input = simpledialog.askstring("Input", "Enter Input: ")
        return user_input
    
    # Restore the stdin
    def restore_stdin(self):
        # restore stdin before closing the application
        sys.stdin = sys.__stdin__
        self.root.destroy()

    def view_parse_tree(self):
        # create a new top-level window
        parse_tree_window = tk.Toplevel(self.root)
        parse_tree_window.title("Parse Tree")

    def execute_code(self):
        if self.file_path:
            with open(self.file_path, 'w') as file:
                file.write(self.text_editor.get("1.0", tk.END))

        # get the lexemes
        self.lexemes = lexer(self.file_path)
        # clear symbol table
        self.symbols = SymbolTable()
        self.parser = Parser(self.lexemes)
        self.tree = self.parser.parse()
        self.interpreter = Interpreter(self.tree, self.symbols)
        self.interpreter.interpret()

        self.variables = self.symbols.variables

        self.populate_lexemes_table()
        self.populate_symbol_table()

    def populate_lexemes_table(self):
        # clear the contents of the table before inserting
        self.lexemes_table.clear_table()

        for lexeme in self.lexemes:
            self.lexemes_table.insert("", "end", values=(lexeme.keyword, lexeme.token_type))

    def populate_symbol_table(self):
        # clear the contents of the table before inserting
        self.symbol_table.clear_table()

        for identifier in self.variables.items():
            self.symbol_table.insert("", "end", values=identifier)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("LOLCODE files", "*.lol"), ("All files", "*.*")])

        if file_path:
            with open(file_path, 'r') as file:
                file_content = file.read()
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(tk.END, file_content)

        self.file_path = file_path

    def create_scrollable_table(self, parent, headers):
        table_frame = tk.Frame(parent)

        # Treeview widget for the table
        table = ttk.Treeview(table_frame, columns=headers, show="headings",selectmode="browse")

        # configure column headings
        for header in headers:
            table.heading(header, text=header)
            table.column(header, anchor="center")

        # Scrollbars for the table
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal",command=table.xview)
        table.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # pack the components 
        table.grid(row = 0, column = 0, sticky="nsew")
        vsb.grid(row = 0, column = 1, sticky="ns")
        hsb.grid(row = 1, column = 0, sticky="ew")

        # Resize configuration
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        # To delete previous contents of the table
        def clear_table():
            table.delete(*table.get_children())

        # attach the clear table method to the table object
        table.clear_table = clear_table

        # return the table frame and table
        return table_frame, table

if __name__ == "__main__":
    root = tk.Tk()
    app = InterpreterGUI(root)
    root.mainloop()
