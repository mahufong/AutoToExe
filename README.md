# Multi-Project Build System

这是一个多项目构建系统，使用GitHub Actions自动构建多个Python项目为Windows可执行文件。

## 项目结构

```
├── .github/workflows/
│   └── build.yml          # GitHub Actions工作流
├── log-classifier/        # 日志分类工具项目
│   └── log_classifier_gui.py
├── example-project/       # 示例项目
│   └── main.py
├── CLAUDE.md             # Claude代码助手配置
└── README.md             # 项目说明文档
```

## 使用方法

### 1. 添加新项目

1. 在根目录创建项目文件夹
2. 在文件夹中放置Python文件（main.py或app.py）
3. 推送到GitHub

### 2. 自动构建

- **推送代码到main分支**: 自动构建所有项目
- **手动触发**: 在GitHub Actions中手动运行工作流
- **指定项目构建**: 可以指定只构建特定项目

### 3. 获取构建结果

构建完成后，在GitHub Actions的Artifacts中下载可执行文件。

## 项目配置

每个项目应该包含：
- 至少一个Python文件
- 使用Tkinter或其他GUI库（可选）
- 可以在Windows上运行
- (可选) `requirements.txt` - 项目依赖包列表

## GitHub Actions

工作流功能：
- 自动检测项目文件夹
- 为每个项目构建独立的EXE文件
- 自动安装项目依赖包（如果存在requirements.txt）
- 支持手动触发
- 在Windows环境中构建（使用PowerShell语法）

### 依赖包管理

每个项目可以包含 `requirements.txt` 文件来指定依赖包：

```txt
# requirements.txt 示例
requests==2.31.0
pandas==2.0.3
numpy==1.24.3
```

GitHub Actions会自动检测并安装这些依赖包。

## 本地开发

```bash
# 安装依赖
pip install pyinstaller

# 构建单个项目
cd log-classifier
pyinstaller --onefile --name LogClassifier log_classifier_gui.py

# 运行程序
dist/LogClassifier.exe
```

## 注意事项

- 确保Python文件有正确的 `if __name__ == "__main__":` 入口
- GUI程序使用 `--windowed` 参数避免控制台窗口
- 大型项目可能需要额外的依赖配置