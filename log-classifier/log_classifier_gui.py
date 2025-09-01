import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import re
import os
import threading

class LogClassifierGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("日志分类工具")
        self.root.geometry("600x400")
        
        self.input_file = tk.StringVar()
        self.output_dir = tk.StringVar(value="sorted_logs")
        self.status_text = tk.StringVar(value="准备就绪")
        
        self.setup_ui()
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        ttk.Label(main_frame, text="输入日志文件:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        # 创建拖放区域
        drop_frame = ttk.Frame(main_frame)
        drop_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        drop_frame.columnconfigure(0, weight=1)
        
        self.input_entry = ttk.Entry(drop_frame, textvariable=self.input_file, width=40)
        self.input_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # 设置拖放提示
        self.input_entry.insert(0, "拖放日志文件到这里或点击浏览...")
        self.input_entry.configure(foreground="gray")
        
        # 绑定拖放事件
        self.setup_drag_drop()
        
        ttk.Button(main_frame, text="浏览...", command=self.browse_input_file).grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Label(main_frame, text="输出目录:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_dir, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        ttk.Button(main_frame, text="浏览...", command=self.browse_output_dir).grid(row=1, column=2, padx=5, pady=5)
        
        self.process_btn = ttk.Button(main_frame, text="开始处理", command=self.start_processing)
        self.process_btn.grid(row=2, column=0, columnspan=3, pady=20)
        
        ttk.Label(main_frame, text="状态:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Label(main_frame, textvariable=self.status_text).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        self.log_text = tk.Text(main_frame, height=15, width=70)
        self.log_text.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.grid(row=5, column=3, sticky=(tk.N, tk.S), pady=10)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        main_frame.rowconfigure(5, weight=1)
    
    def browse_input_file(self):
        filename = filedialog.askopenfilename(
            title="选择日志文件",
            filetypes=[("文本文件", "*.txt"), ("日志文件", "*.log"), ("所有文件", "*.*")]
        )
        if filename:
            self.input_file.set(filename)
            # 清除提示文本
            if self.input_entry.get() == "拖放日志文件到这里或点击浏览...":
                self.input_entry.delete(0, tk.END)
                self.input_entry.configure(foreground="black")
            self.status_text.set(f"已选择文件: {os.path.basename(filename)}")
    
    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="选择输出目录")
        if directory:
            self.output_dir.set(directory)
    
    def setup_drag_drop(self):
        """设置文件拖放功能"""
        # 绑定拖放事件
        self.input_entry.bind("<Button-1>", self.on_entry_click)
        self.input_entry.bind("<DragEnter>", self.on_drag_enter)
        self.input_entry.bind("<DragLeave>", self.on_drag_leave)
        self.input_entry.bind("<Drop>", self.on_drop)
    
    def on_entry_click(self, event):
        """点击输入框时清除提示文本"""
        if self.input_entry.get() == "拖放日志文件到这里或点击浏览...":
            self.input_entry.delete(0, tk.END)
            self.input_entry.configure(foreground="black")
    
    def on_drag_enter(self, event):
        """拖拽进入时的视觉效果"""
        self.input_entry.configure(background="#e0e0e0")
        return True
    
    def on_drag_leave(self, event):
        """拖拽离开时恢复样式"""
        self.input_entry.configure(background="white")
    
    def on_drop(self, event):
        """处理文件拖放"""
        self.input_entry.configure(background="white")
        
        # 获取拖放的文件路径
        file_path = event.data
        
        # 清理路径（移除可能的括号）
        if isinstance(file_path, str):
            file_path = file_path.strip().replace('{', '').replace('}', '')
            
            # 检查是否是有效的文件
            if file_path and os.path.isfile(file_path):
                # 检查文件扩展名
                if file_path.lower().endswith(('.txt', '.log')):
                    self.input_file.set(file_path)
                    self.input_entry.configure(foreground="black")
                    self.status_text.set(f"已选择文件: {os.path.basename(file_path)}")
                else:
                    messagebox.showwarning("警告", "请拖放.txt或.log格式的日志文件")
            else:
                messagebox.showwarning("警告", "请拖放有效的日志文件")
    
    def start_processing(self):
        input_file = self.input_file.get()
        output_dir = self.output_dir.get()
        
        if not input_file:
            messagebox.showerror("错误", "请选择输入文件")
            return
        
        if not output_dir:
            messagebox.showerror("错误", "请指定输出目录")
            return
        
        self.process_btn.config(state='disabled')
        self.progress.start()
        self.status_text.set("正在处理...")
        self.log_text.delete(1.0, tk.END)
        
        thread = threading.Thread(target=self.process_logs, args=(input_file, output_dir))
        thread.daemon = True
        thread.start()
    
    def process_logs(self, input_file, output_dir):
        try:
            self.append_log(f"正在从 '{input_file}' 读取日志...")
            self.append_log(f"分类后的日志将被保存在目录: '{output_dir}/'")
            
            thread_pattern = re.compile(r'^<(\d+):\d+>')
            
            if not os.path.exists(input_file):
                self.append_log(f"错误：输入文件 '{input_file}' 不存在")
                return
            
            os.makedirs(output_dir, exist_ok=True)
            
            open_files = {}
            last_seen_thread_id = None
            no_owner_key = 'no_thread_id_at_start'
            
            with open(input_file, 'r', encoding='utf-8', errors='ignore') as infile:
                total_lines = sum(1 for _ in infile)
                infile.seek(0)
                
                for line_num, line in enumerate(infile, 1):
                    match = thread_pattern.match(line)
                    
                    if match:
                        current_thread_id = match.group(1)
                        last_seen_thread_id = current_thread_id
                    else:
                        current_thread_id = last_seen_thread_id
                    
                    target_key = current_thread_id if current_thread_id else no_owner_key
                    
                    if target_key not in open_files:
                        if target_key == no_owner_key:
                            filename = os.path.join(output_dir, 'no_thread_logs.txt')
                        else:
                            filename = os.path.join(output_dir, f'thread_{target_key}.log')
                        
                        open_files[target_key] = open(filename, 'w', encoding='utf-8')
                        self.append_log(f"创建文件: {os.path.basename(filename)}")
                    
                    open_files[target_key].write(line)
                    
                    if line_num % 1000 == 0:
                        self.append_log(f"已处理 {line_num}/{total_lines} 行")
            
            for file_handle in open_files.values():
                file_handle.close()
            
            self.append_log("\n日志文件处理完成！")
            self.append_log("所有文件已关闭。")
            
            self.root.after(0, self.on_processing_complete, True, "处理完成")
            
        except Exception as e:
            error_msg = f"处理文件时发生错误: {e}"
            self.append_log(error_msg)
            self.root.after(0, self.on_processing_complete, False, error_msg)
    
    def append_log(self, message):
        self.root.after(0, lambda: self.log_text.insert(tk.END, message + "\n"))
        self.root.after(0, lambda: self.log_text.see(tk.END))
    
    def on_processing_complete(self, success, message):
        self.progress.stop()
        self.process_btn.config(state='normal')
        self.status_text.set(message)
        
        if success:
            messagebox.showinfo("完成", "日志处理完成！")
        else:
            messagebox.showerror("错误", message)

def main():
    root = tk.Tk()
    app = LogClassifierGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()