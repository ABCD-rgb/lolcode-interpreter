import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
from lexer import lexer


class InterpreterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Interpreter GUI")
        self.file_path = ""

        # File Explorer
        self.file_explorer_button = tk.Button(root, text="Open File", command=self.open_file)
        self.file_explorer_button.grid(row=0, column=0, pady=2)

        # labels
        self.tokens_label = tk.Label(root, text="Lexemes")
        self.tokens_label.grid(row=0, column=1, pady=2)

        self.symbol_table_label = tk.Label(root, text="Symbol Table")
        self.symbol_table_label.grid(row=0, column=2, pady=2)

        # Text Editor
        self.text_editor = scrolledtext.ScrolledText(root, width=40, height=20)
        self.text_editor.grid(row=1, column=0, pady=2, padx=2, sticky="nsew")

        # List of Tokens
        self.tokens_list = self.create_scrollable_table(root, headers=["Lexeme", "Classification"])
        self.tokens_list.grid(row=1, column=1, pady=2, padx=2, sticky="nsew")

        # Symbol Table
        self.symbol_table = self.create_scrollable_table(root, headers=["Identifier", "Value"])
        self.symbol_table.grid(row=1, column=2, pady=2, padx=2, sticky="nsew")

        # Execute Button
        self.execute_button = tk.Button(root, text="Execute", command=self.execute_code)
        self.execute_button.grid(row=2, column=0, pady=2)

        # Console
        self.console = scrolledtext.ScrolledText(root, width=80, height=20)
        self.console.grid(row=3, column=0, columnspan=3, pady=2, padx=5, sticky="ew")

        # Configure row and column weights for resizing
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(2, weight=1)
        root.grid_rowconfigure(3, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)


    def execute_code(self):
        if self.file_path:
            with open(self.file_path, 'w') as file:
                file.write(self.text_editor.get("1.0", tk.END))

        lexemes = lexer(self.file_path)

        print(lexemes)

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

        return table_frame

if __name__ == "__main__":
    root = tk.Tk()
    app = InterpreterGUI(root)
    root.mainloop()
