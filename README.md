# Multi-Project Build System

这是一个多项目构建系统，使用GitHub Actions自动构建多个Python项目为Windows可执行文件。支持自动测试、依赖管理和多项目并行构建。

## 项目结构

```
├── .github/workflows/
│   └── build.yml          # GitHub Actions工作流（自动测试+构建）
├── log-classifier/        # 日志分类工具项目（PyQt5 GUI）
│   ├── log_classifier_qt.py     # 主程序文件
│   ├── requirements.txt         # 项目依赖（PyQt5）
│   └── test_log_classifier.py   # 自动化测试
├── example-project/       # 示例项目
│   └── main.py
└── README.md             # 项目说明文档
```

## 使用方法

### 1. 添加新项目

1. 在根目录创建项目文件夹
2. 在文件夹中放置Python文件（main.py或app.py）
3. （可选）添加 `requirements.txt` 指定依赖包
4. （可选）添加 `test_*.py` 文件进行自动化测试
5. 推送到GitHub

### 2. 自动构建流程

1. **自动测试**: 运行所有项目的 `test_*.py` 测试文件
2. **依赖安装**: 自动安装 `requirements.txt` 中的依赖包
3. **构建EXE**: 使用PyInstaller构建Windows可执行文件
4. **上传产物**: 构建结果上传到GitHub Actions Artifacts

### 3. 触发方式

- **推送代码到master分支**: 自动触发完整构建流程
- **Pull Request**: 自动运行测试确保代码质量
- **手动触发**: 在GitHub Actions中手动运行工作流

### 4. 获取构建结果

构建完成后，在GitHub Actions的Artifacts中下载可执行文件。

## 项目配置

每个项目应该包含：
- 至少一个Python文件（支持多种命名：main.py、app.py、或自定义名称）
- 支持GUI框架：PyQt5、Tkinter等
- Windows兼容性：确保代码在Windows上正常运行
- (可选) `requirements.txt` - 项目依赖包列表
- (可选) `test_*.py` - 自动化测试文件

## GitHub Actions

工作流功能：
- **自动测试**: 运行所有项目的自动化测试（test_*.py）
- **依赖管理**: 自动安装requirements.txt中的依赖包
- **智能构建**: 优先构建Qt版本程序，支持多种命名约定
- **多项目支持**: 自动检测并构建所有项目文件夹
- **Windows环境**: 在Windows Server 2022环境中构建
- **产物管理**: 自动上传可执行文件到Artifacts

### 依赖包管理

每个项目可以包含 `requirements.txt` 文件来指定依赖包：

```txt
# requirements.txt 示例
PyQt5==5.15.9           # GUI框架
requests==2.31.0        # HTTP请求
pandas==2.0.3           # 数据处理
numpy==1.24.3           # 数值计算
```

GitHub Actions会自动检测并安装这些依赖包。支持PyQt5等需要系统依赖的库。

## 本地开发（可选）

```bash
# 安装依赖（如果需要本地测试）
pip install pyinstaller PyQt5

# 构建PyQt5项目
cd log-classifier
pyinstaller --onefile --name LogClassifier --windowed --icon=icon.ico --noconsole log_classifier_qt.py

# 运行程序
dist/LogClassifier.exe

# 运行测试
python test_log_classifier.py
```

> 注意：推荐使用GitHub Actions进行构建，无需本地Python环境

## 注意事项

- 确保Python文件有正确的 `if __name__ == "__main__":` 入口
- GUI程序使用 `--windowed` 和 `--noconsole` 参数避免控制台窗口
- 使用 `--icon=icon.ico` 为程序添加自定义图标
- 避免在测试中使用Unicode符号（✓/✗），使用PASS/FAIL文本
- PyQt5程序需要正确的线程处理，避免UI卡顿
- 大型项目可能需要额外的系统依赖配置

## 当前项目示例：日志分类工具

### 功能特点
- **文件拖放**: 支持将日志文件直接拖放到程序界面
- **多线程处理**: 后台处理日志，界面保持响应
- **实时进度**: 显示处理进度和状态信息
- **自动分类**: 根据线程ID自动分类日志到不同文件
- **错误处理**: 完善的错误提示和日志输出

### 技术栈
- **GUI框架**: PyQt5 (现代化原生界面)
- **多线程**: threading + Qt信号槽机制
- **文件处理**: 正则表达式匹配 + 动态文件管理
- **构建工具**: PyInstaller + GitHub Actions

### 使用方式
1. 运行程序后，拖放日志文件到输入框或点击浏览选择
2. 指定输出目录（默认为sorted_logs）
3. 点击"开始处理"按钮
4. 查看实时处理日志和进度
5. 处理完成后在输出目录查看分类结果