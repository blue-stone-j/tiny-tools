import json
import tkinter as tk
from tkinter import ttk

# 读取JSON文件
def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
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

# 创建窗口
root = tk.Tk()
root.title('JSON Tree View')

# 创建树形视图
tree = ttk.Treeview(root)
tree.pack(expand=True, fill='both')

# 加载JSON数据
data = load_json('map.json')
add_tree_item('', data)  # '' 表示从根节点开始添加

# 启动GUI
root.mainloop()

