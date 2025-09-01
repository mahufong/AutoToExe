#!/usr/bin/env python3
"""
示例项目 - 简单的文本处理工具
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def main():
    root = tk.Tk()
    root.title("示例工具")
    root.geometry("400x300")
    
    frame = ttk.Frame(root, padding="20")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    label = ttk.Label(frame, text="这是一个示例项目")
    label.grid(row=0, column=0, pady=10)
    
    button = ttk.Button(frame, text="点击我", command=lambda: messagebox.showinfo("信息", "Hello from example project!"))
    button.grid(row=1, column=0, pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    main()