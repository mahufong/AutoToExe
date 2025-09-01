#!/usr/bin/env python3
"""
Log Classifier GUI using PyQt5 with proper drag-drop and progress functionality
"""

import sys
import os
import re
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton, QProgressBar, QTextEdit,
                             QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QDragEnterEvent, QDropEvent


class WorkerSignals(QObject):
    """Defines the signals available from a running worker thread."""
    finished = pyqtSignal()
    error = pyqtSignal(str)
    progress = pyqtSignal(int, int)  # current, total
    log = pyqtSignal(str)


class LogProcessor(threading.Thread):
    """Worker thread for processing logs."""
    
    def __init__(self, input_file, output_dir):
        super().__init__()
        self.input_file = input_file
        self.output_dir = output_dir
        self.signals = WorkerSignals()
        
    def run(self):
        try:
            self.signals.log.emit(f"正在从 '{self.input_file}' 读取日志...")
            self.signals.log.emit(f"分类后的日志将被保存在目录: '{self.output_dir}/'")
            
            thread_pattern = re.compile(r'^<(\d+):\d+>')
            
            if not os.path.exists(self.input_file):
                self.signals.log.emit(f"错误：输入文件 '{self.input_file}' 不存在")
                return
            
            os.makedirs(self.output_dir, exist_ok=True)
            
            open_files = {}
            last_seen_thread_id = None
            no_owner_key = 'no_thread_id_at_start'
            
            with open(self.input_file, 'r', encoding='utf-8', errors='ignore') as infile:
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
                            filename = os.path.join(self.output_dir, 'no_thread_logs.txt')
                        else:
                            filename = os.path.join(self.output_dir, f'thread_{target_key}.log')
                        
                        open_files[target_key] = open(filename, 'w', encoding='utf-8')
                        self.signals.log.emit(f"创建文件: {os.path.basename(filename)}")
                    
                    open_files[target_key].write(line)
                    
                    if line_num % 1000 == 0:
                        self.signals.progress.emit(line_num, total_lines)
                        self.signals.log.emit(f"已处理 {line_num}/{total_lines} 行")
            
            for file_handle in open_files.values():
                file_handle.close()
            
            self.signals.log.emit("\n日志文件处理完成！")
            self.signals.log.emit("所有文件已关闭。")
            self.signals.finished.emit()
            
        except Exception as e:
            self.signals.error.emit(f"处理文件时发生错误: {e}")


class LogClassifierGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("日志分类工具")
        self.setGeometry(100, 100, 800, 600)
        
        self.input_file = ""
        self.output_dir = "sorted_logs"
        self.worker = None
        
        self.setup_ui()
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Input file section
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("输入日志文件:"))
        
        self.input_entry = QLineEdit()
        self.input_entry.setPlaceholderText("拖放日志文件到这里或点击浏览...")
        self.input_entry.setReadOnly(True)
        self.input_entry.setAcceptDrops(True)
        self.input_entry.dragEnterEvent = self.drag_enter_event
        self.input_entry.dropEvent = self.drop_event
        input_layout.addWidget(self.input_entry)
        
        browse_btn = QPushButton("浏览...")
        browse_btn.clicked.connect(self.browse_input_file)
        input_layout.addWidget(browse_btn)
        
        layout.addLayout(input_layout)
        
        # Output directory section
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("输出目录:"))
        
        self.output_entry = QLineEdit(self.output_dir)
        output_layout.addWidget(self.output_entry)
        
        output_browse_btn = QPushButton("浏览...")
        output_browse_btn.clicked.connect(self.browse_output_dir)
        output_layout.addWidget(output_browse_btn)
        
        layout.addLayout(output_layout)
        
        # Process button
        self.process_btn = QPushButton("开始处理")
        self.process_btn.clicked.connect(self.start_processing)
        layout.addWidget(self.process_btn)
        
        # Status
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("状态:"))
        
        self.status_label = QLabel("准备就绪")
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        
        layout.addLayout(status_layout)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # Log output
        layout.addWidget(QLabel("处理日志:"))
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)
    
    def drag_enter_event(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def drop_event(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.lower().endswith(('.txt', '.log')):
                self.input_file = file_path
                self.input_entry.setText(os.path.basename(file_path))
                self.status_label.setText(f"已选择文件: {os.path.basename(file_path)}")
            else:
                QMessageBox.warning(self, "警告", "请拖放.txt或.log格式的日志文件")
    
    def browse_input_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "选择日志文件", "", "文本文件 (*.txt);;日志文件 (*.log);;所有文件 (*.*)"
        )
        if filename:
            self.input_file = filename
            self.input_entry.setText(os.path.basename(filename))
            self.status_label.setText(f"已选择文件: {os.path.basename(filename)}")
    
    def browse_output_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if directory:
            self.output_dir = directory
            self.output_entry.setText(directory)
    
    def start_processing(self):
        if not self.input_file:
            QMessageBox.critical(self, "错误", "请选择输入文件")
            return
        
        self.output_dir = self.output_entry.text() or "sorted_logs"
        
        self.process_btn.setEnabled(False)
        self.status_label.setText("正在处理...")
        self.progress_bar.setValue(0)
        self.log_text.clear()
        
        self.worker = LogProcessor(self.input_file, self.output_dir)
        self.worker.signals.finished.connect(self.on_processing_complete)
        self.worker.signals.error.connect(self.on_processing_error)
        self.worker.signals.progress.connect(self.on_progress_update)
        self.worker.signals.log.connect(self.append_log)
        self.worker.start()
    
    def on_progress_update(self, current, total):
        progress = int((current / total) * 100) if total > 0 else 0
        self.progress_bar.setValue(progress)
    
    def append_log(self, message):
        self.log_text.append(message)
        # Auto-scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def on_processing_complete(self):
        self.process_btn.setEnabled(True)
        self.status_label.setText("处理完成")
        self.progress_bar.setValue(100)
        QMessageBox.information(self, "完成", "日志处理完成！")
    
    def on_processing_error(self, error_msg):
        self.process_btn.setEnabled(True)
        self.status_label.setText("处理失败")
        self.append_log(error_msg)
        QMessageBox.critical(self, "错误", error_msg)


def main():
    app = QApplication(sys.argv)
    window = LogClassifierGUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()