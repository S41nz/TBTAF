import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import code

class CustomInterpreter(code.InteractiveInterpreter):
    def __init__(self, locals=None):
        super().__init__(locals)
        self.output = ""

    def write(self, data):
        self.output += str(data)

class CustomIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Python IDE")
        self.root.state("zoomed")

        self.interpreter = CustomInterpreter(locals)
        # print('hello!')
        # exec(open('./tbtaf/tbtaf_launcher.py').read())

        # Track whether the file has been modified
        self.file_modified = False
        self.current_file_path = None

        # Tabs
        self.tab_id_counter = 1
        self.opened_tabs = set()
        self.tab_states = {}

        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)
        self.root.bind("<Control-s>", self.save_file)
        self.root.bind("<Control-Shift-s>", self.save_file_as)
        # Set the size of the sidebar
        sidebar_width = self.root.winfo_screenwidth() // 5
        

        # Create and place the PanedWindow
        self.paned_window = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashwidth=5, sashrelief=tk.RAISED)
        self.paned_window.pack(expand=True, fill=tk.BOTH)

        # Create and place the sidebar
        self.sidebar = tk.Frame(self.paned_window, bg="lightblue", width=sidebar_width)
        sidebar_title = tk.Label(self.sidebar, text="File Explorer", bg="lightblue")
        sidebar_title.pack(pady=5)
        self.directory_tree = ttk.Treeview(self.sidebar)
        self.directory_tree.pack(expand=True, fill=tk.Y)

        self.paned_window.add(self.sidebar)

        # Create another PanedWindow for the vertical split
        self.vertical_paned_window = tk.PanedWindow(self.paned_window, orient=tk.VERTICAL, sashwidth=5, sashrelief=tk.RAISED)
        self.notebook = ttk.Notebook(self.vertical_paned_window, height=700)
        self.vertical_paned_window.add(self.notebook)
        editor_title = tk.Label(self.vertical_paned_window, text="Editor")
        editor_title.pack()

        # Create a Notebook for the editor

        # Create and place the terminal
        self.terminal = tk.Text(self.vertical_paned_window, wrap="word")
        self.vertical_paned_window.add(self.terminal)

        # Add the vertical PanedWindow to the main PanedWindow
        self.paned_window.add(self.vertical_paned_window)

        # Bind file editor changes
        self.directory_tree.bind("<Double-1>", self.open_selected_file)
        self.terminal.bind("<Return>", lambda event: self.execute_code())
        # self.file_editor_text.bind("<Key>", self.mark_file_as_modified)

        self.update_directory_tree()
    
            # Menu setup
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_tab)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)

    def add_or_select_tab(self, tab_name, text_content):
        # Check if a tab with the same name is already open
        for tab_id in self.opened_tabs:
            tab_state = self.tab_states[tab_id]
            if tab_state["tab_name"] == tab_name:
                # Tab with the same name is already open, select it and return
                self.notebook.select(tab_state["id"])
                return

        # If the tab is not already open, add a new tab
        tab_id = self.tab_id_counter
        self.tab_id_counter += 1

        new_tab = tk.Frame(self.notebook)
        scrolled_text = scrolledtext.ScrolledText(new_tab, wrap="word", width=50, height=20)
        scrolled_text.insert(tk.END, text_content)
        scrolled_text.pack(fill=tk.BOTH, expand=True)

        # Bind the Key event to the text widget to track changes
        # scrolled_text.bind("<Key>", lambda event, tab_id=tab_id: self.on_text_change(event, tab_id))

        self.notebook.add(new_tab, text=tab_name)
        self.opened_tabs.add(tab_id)

        # Store the tab state
        self.tab_states[tab_id] = {"id": self.notebook.index(new_tab), "tab_name": tab_name, "content": text_content, "widget": scrolled_text}
        self.notebook.select(new_tab)

    # def on_text_change(self, event, tab_id):
        # This function will be called when the text in a tab changes
        # print(f"Text in tab {tab_id} changed!")

    def new_tab(self):
        self.add_or_select_tab("New Tab", "")

    
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
            self.add_or_select_tab(file_path, content)

    def save_file(self, event=None):
        current_tab_id = self.get_current_tab_id()
        if current_tab_id is not None:
            current_tab_state = self.get_tab_state(current_tab_id)
            print(current_tab_state["file_path"])
            if "file_path" in current_tab_state:
                # File has been saved before, save the changes
                file_path = current_tab_state["file_path"]
                content = current_tab_state["widget"].get("1.0", tk.END)
                with open(file_path, "w") as file:
                    file.write(content)
            else:
                # No file path, use "Save As" to specify a file path
                self.save_file_as()

    def save_file_as(self, event=None):
        current_tab_id = self.get_current_tab_id()
        if current_tab_id is not None:
            current_tab_state = self.get_tab_state(current_tab_id)
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if file_path:
                # Save the file
                content = current_tab_state["widget"].get("1.0", tk.END)
                with open(file_path, "w") as file:
                    file.write(content)

                # Update the tab state with the file path
                current_tab_state["file_path"] = file_path
                current_tab_state["tab_name"] = file_path
                self.notebook.tab(current_tab_state["id"], text=file_path)

    def get_current_tab_id(self):
        current_tab_index = self.notebook.index(self.notebook.select())
        for tab_id, tab_state in self.tab_states.items():
            if tab_state["id"] == current_tab_index:
                return tab_id
        return None

    def get_tab_state(self, tab_id):
        return self.tab_states.get(tab_id, {})

    def set_tab_state(self, tab_id, tab_state):
        self.tab_states[tab_id] = tab_state

    def update_directory_tree(self):
        self.directory_tree.delete(*self.directory_tree.get_children())
        current_directory = os.getcwd()

        root_node = self.directory_tree.insert("", "end", text=current_directory, open=True)
        self.populate_tree(root_node, current_directory)

    def populate_tree(self, parent, path):
        try:
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                is_directory = os.path.isdir(full_path)

                node = self.directory_tree.insert(parent, "end", text=item, open=False, values=(full_path,))
                
                if is_directory:
                    self.populate_tree(node, full_path)
                else:
                    self.directory_tree.bind("<ButtonRelease-1>", self.open_selected_file)
        except Exception as e:
            print(f"Error populating tree: {str(e)}")

    def open_selected_file(self, event):
        item_id = self.directory_tree.selection()[0]
        item_values = self.directory_tree.item(item_id, "values")

        if item_values and os.path.isfile(item_values[0]):
            file_path = item_values[0]

            with open(file_path, 'r') as file:
                content = file.read()
                self.add_or_select_tab(os.path.basename(file_path), content)

    def close_window(self):
        if self.file_modified:
            response = messagebox.askyesnocancel("Save Changes", "Do you want to save changes before closing?")
            
            if response is None:
                return  # User canceled
            elif response:
                self.save_file(None)  # Save changes before closing
        self.root.destroy()

    def execute_console_command(self, event):
        command = self.terminal.get("insert linestart", "insert lineend")
        self.terminal.insert(tk.END, '\n')
        self.interpreter.runsource(command)

    def run_code(self, command, locals):
        interpreter = CustomInterpreter(locals)
        interpreter.runsource(command)
        return interpreter.output

    def execute_code(self, event=None):
        command = self.terminal.get("1.0", tk.END).strip()
        output = self.run_code(command, globals())
        self.terminal.delete("1.0", tk.END)
        self.terminal.insert(tk.END, output)

    def display_current_directory(self):
        current_directory = os.getcwd()
        self.terminal.insert(tk.END, f"\n\nCurrent Directory: {current_directory}")

if __name__ == "__main__":
    root = tk.Tk()
    ide = CustomIDE(root)
    root.mainloop()
