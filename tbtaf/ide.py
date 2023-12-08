import os
import code
import subprocess
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk
import sys

class CustomInterpreter(code.InteractiveInterpreter):
    def __init__(self, locals=None):
        super().__init__(locals)
        self.output = ""

    def write(self, data):
        self.output += str(data)

class TkinterIDEApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter IDE")
        self.root.geometry("800x600")

        # Main Frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        # PanedWindow for Explorer and Editor & Terminal
        self.paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(expand=True, fill=tk.BOTH)

        # Sidebar (Directory Viewer)
        self.sidebar_frame = ttk.Frame(self.paned_window, width=200)
        self.paned_window.add(self.sidebar_frame)

        self.directory_label = tk.Label(self.sidebar_frame, text="Current Directory:")
        self.directory_label.pack()

        self.directory_tree = ttk.Treeview(self.sidebar_frame)
        self.directory_tree.pack(expand=True, fill=tk.Y)

        self.update_directory_tree()

        # Editor and Terminal Frame
        self.terminal_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.terminal_frame)

        # File Editor
        self.file_editor_frame = ttk.Frame(self.paned_window)
        self.paned_window.add(self.file_editor_frame, weight=1)

        self.file_editor_text = scrolledtext.ScrolledText(self.file_editor_frame, wrap=tk.WORD)
        self.file_editor_text.pack(expand=True, fill=tk.BOTH)

        # Command Entry
        self.command_label = tk.Label(self.terminal_frame, text="Enter Command:")
        self.command_label.pack()

        # PanedWindow for Editor & Terminal
        self.terminal_frame = ttk.PanedWindow(self.terminal_frame, orient=tk.HORIZONTAL)
        self.terminal_frame.pack(expand=True, fill=tk.BOTH)

        # Interactive Python Console
        self.python_console_frame = ttk.Frame(self.terminal_frame)
        self.terminal_frame.add(self.python_console_frame, weight=1)

        self.python_console_text = scrolledtext.ScrolledText(self.python_console_frame, wrap=tk.WORD)
        self.python_console_text.pack(expand=True, fill=tk.BOTH)

        self.interpreter = CustomInterpreter(locals)
        self.python_console_text.bind("<Return>", lambda event: self.execute_code())

        # print('hello!')
        # exec(open('./tbtaf/tbtaf_launcher.py').read())

        # Open File Button
        self.directory_tree.bind("<Double-1>", self.open_selected_file)

        # Save File Button
        self.file_editor_text.bind("<Control-s>", self.save_file)

        # Track whether the file has been modified
        self.file_modified = False
        self.current_file_path = None

        # Tabs
        self.tabs = {}  # Dictionary to store tabs {tab_id: file_path}

        # Bind file editor changes
        self.file_editor_text.bind("<Key>", self.mark_file_as_modified)

        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

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
        if self.file_modified:
            response = messagebox.askyesnocancel("Save Changes", "Do you want to save changes before opening a new file?")
            
            if response is None:
                return  # User canceled
            elif response:
                self.save_file(None)  # Save changes before opening a new file

        item_id = self.directory_tree.selection()[0]
        item_values = self.directory_tree.item(item_id, "values")

        if item_values and os.path.isfile(item_values[0]):
            file_path = item_values[0]

            with open(file_path, 'r') as file:
                content = file.read()
                self.file_editor_text.delete(1.0, tk.END)
                self.file_editor_text.insert(tk.END, content)

                self.current_file_path = file_path
                self.file_modified = False

                # Add tab
                self.add_tab(file_path, os.path.basename(file_path))

    def save_file(self, event):
        if self.current_file_path:
            content = self.file_editor_text.get(1.0, tk.END)
            with open(self.current_file_path, 'w') as file:
                file.write(content)
            messagebox.showinfo("File Saved", f"File saved successfully to {self.current_file_path}")
            self.file_modified = False
        else:
            self.save_file_as(event)

    def save_file_as(self, event):
        file_path = filedialog.asksaveasfilename()

        if file_path:
            content = self.file_editor_text.get(1.0, tk.END)
            with open(file_path, 'w') as file:
                file.write(content)
            messagebox.showinfo("File Saved", f"File saved successfully to {file_path}")
            self.current_file_path = file_path
            self.file_modified = False

            # Add tab
            self.add_tab(file_path, os.path.basename(file_path))

    def add_tab(self, file_path, tab_title):
        tab_id = self.notebook.add(self.terminal_frame, text=tab_title)
        close_button = tk.Button(self.top_bar_frame, text="x", command=lambda: self.close_tab(tab_id, file_path))
        close_button.grid(row=0, column=len(self.tabs))
        self.tabs[tab_id] = file_path
        self.notebook.select(tab_id)

    def close_tab(self, tab_id, file_path):
        self.notebook.forget(tab_id)
        del self.tabs[tab_id]
        if self.tabs:
            self.notebook.select(list(self.tabs.keys())[-1])
        else:
            self.current_file_path = None
            self.file_editor_text.delete(1.0, tk.END)

    def mark_file_as_modified(self, event):
        self.file_modified = True

    def close_window(self):
        if self.file_modified:
            response = messagebox.askyesnocancel("Save Changes", "Do you want to save changes before closing?")
            
            if response is None:
                return  # User canceled
            elif response:
                self.save_file(None)  # Save changes before closing
        self.root.destroy()

    def execute_console_command(self, event):
        command = self.python_console_text.get("insert linestart", "insert lineend")
        self.python_console_text.insert(tk.END, '\n')
        self.interpreter.runsource(command)
 
    def run_code(self, command, locals):
        interpreter = CustomInterpreter(locals)
        interpreter.runsource(command)
        return interpreter.output

    def execute_code(self, event=None):
        command = self.python_console_text.get("1.0", tk.END).strip()
        output = self.run_code(command, globals())
        self.python_console_text.delete("1.0", tk.END)
        self.python_console_text.insert(tk.END, output)

    def display_current_directory(self):
        current_directory = os.getcwd()
        self.python_console_text.insert(tk.END, f"\n\nCurrent Directory: {current_directory}")

# Create the Tkinter root window
root = tk.Tk()

# Initialize the Tkinter IDE app
ide_app = TkinterIDEApp(root)

# Run the Tkinter event loop
root.mainloop()
