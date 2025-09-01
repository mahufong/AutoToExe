# 程序图标设置指南

## 如何为程序添加自定义图标

### 1. 图标文件要求
- 格式: `.ico` (Windows图标格式)
- 推荐尺寸: 包含多种尺寸 (256x256, 64x64, 32x32, 16x16)
- 位置: 放在项目根目录，命名为 `icon.ico`

### 2. 获取图标文件的方法

#### 方法一: 在线转换工具
1. 准备一个PNG图像 (推荐512x512或256x256)
2. 使用在线转换工具:
   - https://icoconvert.com/
   - https://convertio.co/zh/png-ico/
   - https://www.icoconverter.com/
3. 下载转换后的ICO文件
4. 重命名为 `icon.ico` 并放到项目目录

#### 方法二: 使用图像编辑软件
- Adobe Photoshop
- GIMP (免费)
- Paint.NET (免费)

#### 方法三: 使用Python生成 (高级)
```python
from PIL import Image

# 创建一个简单的程序图标
img = Image.new('RGBA', (256, 256), (0, 120, 215, 255))  # 蓝色背景
img.save('icon.ico', format='ICO', sizes=[(256,256), (64,64), (32,32), (16,16)])
```

### 3. 图标设计建议
- 使用简洁的设计
- 高对比度，确保在不同背景下都清晰可见
- 正方形比例
- 避免过多细节（小尺寸时会模糊）

### 4. 验证图标

构建完成后，可执行文件将自动使用图标。您可以通过以下方式验证：

1. 在Windows文件资源管理器中查看EXE文件
2. 右键 → 属性 → 详细信息，查看图标信息
3. 确保图标在不同显示设置下都清晰

### 5. 现有项目图标状态

当前项目已配置支持图标功能：
- GitHub Actions会自动检测并使用 `icon.ico` 文件
- 如果找不到图标文件，会使用默认图标
- 控制台窗口已隐藏 (`--noconsole` 参数)
- 程序以纯GUI模式运行 (`--windowed` 参数)

### 6. 故障排除

如果图标没有显示：
1. 确认ICO文件格式正确
2. 确认文件名为 `icon.ico`
3. 确认文件放在项目根目录
4. 检查ICO文件是否包含多种尺寸

### 7. 推荐资源

- **免费图标网站**:
  - Flaticon: https://www.flaticon.com/
  - Icons8: https://icons8.com/icons
  - Material Design Icons: https://materialdesignicons.com/

- **图标设计工具**:
  - Figma (免费): https://www.figma.com/
  - Inkscape (免费): https://inkscape.org/
  - Canva (在线): https://www.canva.com/

## 当前配置

构建命令已更新为：
```bash
pyinstaller --onefile --name LogClassifier --windowed --icon=icon.ico --noconsole log_classifier_qt.py
```

- `--windowed`: 隐藏控制台窗口
- `--noconsole`: 不显示命令行窗口
- `--icon=icon.ico`: 使用自定义图标