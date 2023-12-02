import tkinter as tk
from tkinter import ttk
import subprocess

class PySCI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python IDE")

        # File Tree
        self.file_tree = ttk.Treeview(self.root)
        self.file_tree.insert("", "end", text="Project", open=True)
        self.file_tree.insert("Project", "end", text="script1.py")
        self.file_tree.insert("Project", "end", text="script2.py")
        self.file_tree.pack(side=tk.LEFT, fill=tk.Y)

        # Tabbed Editor
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Integrated Terminal
        self.terminal = tk.Text(self.root, wrap=tk.WORD)
        self.terminal.pack(fill=tk.BOTH, expand=True)

        # Execute Button
        execute_button = tk.Button(self.root, text="Execute", command=self.execute_script)
        execute_button.pack()

    def execute_script(self):
        selected_item = self.file_tree.selection()
        if selected_item:
            script_name = self.file_tree.item(selected_item, "text")
            command = f"python {script_name}"  # Modify as needed
            output = subprocess.check_output(command, shell=True, text=True)
            self.terminal.insert(tk.END, output)

if __name__ == "__main__":
    root = tk.Tk()
    app = PySCI(root)
    root.mainloop()