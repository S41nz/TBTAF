import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import subprocess
import os

class TkinterIDEApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python IDE")

        self.sidebar_frame = ttk.Frame(self, width=200, padding=(5, 5, 0, 5))
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.file_tree = ttk.Treeview(self.sidebar_frame, show="tree", selectmode="browse")
        self.file_tree.heading("#0", text="Files")
        self.file_tree.pack(expand=True, fill=tk.BOTH)
        self.load_folder_tree(".")

        self.tab_notebook = ttk.Notebook(self)
        self.tab_notebook.pack(expand=True, fill=tk.BOTH)

        self.create_new_tab()

        self.terminal_frame = ttk.Frame(self, height=200)
        self.terminal_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.terminal = scrolledtext.ScrolledText(self.terminal_frame, wrap=tk.WORD, font=("Courier New", 12))
        self.terminal.pack(expand=True, fill=tk.BOTH)
        self.terminal.insert(tk.END, "root$: ")

        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.create_new_tab)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_application)

        run_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="Run in Terminal", command=self.run_in_terminal)

        self.bind_shortcuts()
        # Bind the tree item selection event to open the selected file in a new tab
        self.file_tree.bind("<<TreeviewSelect>>", self.open_selected_file)

    def create_new_tab(self,):
        tab = ttk.Frame(self.tab_notebook)
        text_widget = scrolledtext.ScrolledText(tab, wrap=tk.WORD, font=("Courier New", 12))
        text_widget.pack(expand=True, fill=tk.BOTH)
        self.tab_notebook.add(tab, text="Untitled")

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
            self.create_new_tab()
            current_tab = self.tab_notebook.tabs()[-1]
            text_widget = self.tab_notebook.nametowidget(current_tab).winfo_children()[0]
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, content)
            self.tab_notebook.tab(current_tab, text=os.path.basename(file_path))

    def open_selected_file(self, event):
        selected_item = self.file_tree.selection()
        if selected_item:
            file_path = self.file_tree.item(selected_item, "text")
            if os.path.isfile(file_path):
                self.create_new_tab()
                current_tab = self.tab_notebook.tabs()[-1]
                tab_widget = self.tab_notebook.nametowidget(current_tab)
                # Check if the child widget is a ScrolledText widget
                if isinstance(tab_widget.winfo_children()[0], scrolledtext.ScrolledText):
                    text_widget = tab_widget.winfo_children()[0]
                    text_widget.delete(1.0, tk.END)
                    with open(file_path, "r") as file:
                        content = file.read()
                    text_widget.insert(tk.END, content)
                    self.tab_notebook.tab(current_tab, text=os.path.basename(file_path))

    def save_file(self):
        current_tab = self.tab_notebook.select()
        text_widget = self.tab_notebook.nametowidget(current_tab).winfo_children()[0]
        content = text_widget.get(1.0, tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(content)
            self.tab_notebook.tab(current_tab, text=os.path.basename(file_path))

    def save_file_as(self):
        current_tab = self.tab_notebook.select()
        text_widget = self.tab_notebook.nametowidget(current_tab).winfo_children()[0]
        content = text_widget.get(1.0, tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python Files", "*.py")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(content)
            self.create_new_tab()
            current_tab = self.tab_notebook.tabs()[-1]
            text_widget = self.tab_notebook.nametowidget(current_tab).winfo_children()[0]
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, content)
            self.tab_notebook.tab(current_tab, text=os.path.basename(file_path))

    def exit_application(self):
        self.destroy()

    def bind_shortcuts(self):
        self.bind("<Control-n>", lambda event: self.create_new_tab())
        self.bind("<Control-o>", lambda event: self.open_file())
        self.bind("<Control-s>", lambda event: self.save_file())
        self.bind("<Control-Shift-s>", lambda event: self.save_file_as())
        self.bind("<Control-q>", lambda event: self.exit_application())
        self.bind("<Return>", lambda event: self.run_in_terminal())

    def run_in_terminal(self):
        full_text = self.terminal.get(1.0, tk.END)
        start_index = full_text.find("root$: ")
        code_to_run = full_text[start_index + len("root$: "):]
        process = subprocess.Popen(
            ["python", "-c", code_to_run],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            self.terminal.insert(tk.END, f"\nOutput: {stdout}\nroot$: ")
        else:
            self.terminal.insert(tk.END, f"\nError: {stderr}\nroot$: ")

    def load_folder_tree(self, folder_path):
        def insert_node(parent, item):
            return self.file_tree.insert(parent, "end", text=item, open=False)

        def traverse_path(path, parent=""):
            items = os.listdir(path)
            for item in sorted(items):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    node = insert_node(parent, item)
                    traverse_path(item_path, parent=node)
                else:
                    insert_node(parent, item)

        traverse_path(folder_path)

# Create the Tkinter root window
root = tk.Tk()
# Initialize the Tkinter IDE app
ide_app = TkinterIDEApp(root)
# Run the Tkinter event loop
root.mainloop()