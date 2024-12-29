import tkinter as tk
from tkinter import ttk
import json

def load_json():
    # Load your JSON data (can be from a file or a string)
    with open("../data/json.json", "r") as file:
        return json.load(file)

# 递归添加树节点
def add_tree_item(parent, data):
    if isinstance(data, dict):
        for key, value in data.items():
            node = tree.insert(parent, 'end', text=key, open=False)
            add_tree_item(node, value)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            node = tree.insert(parent, 'end', text=str(index), open=False)
            add_tree_item(node, item)
    else:
        tree.insert(parent, 'end', text=str(data), open=False)

# Create the main window
root = tk.Tk()
root.title("JSON Tree View")

# Ensure the window expands to fit the content
root.grid_rowconfigure(0, weight=1)  # Allow row to expand
root.grid_columnconfigure(0, weight=1)  # Allow column to expand
root.geometry("800x600") 

# Create a frame to hold the treeview and scrollbar
frame = tk.Frame(root)
frame.grid(row=0, column=0, sticky="nsew")  # Use grid to make it expand

# Create the treeview widget
tree = ttk.Treeview(frame)
tree.pack(side="left", fill="both", expand=True)

# Create a scrollbar linked to the treeview
scrollbar = tk.Scrollbar(frame, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")
tree.configure(yscrollcommand=scrollbar.set)

# Load and build the treeview from the JSON data
json_data = load_json()
add_tree_item('', json_data)

# Start the Tkinter event loop
root.mainloop()