# YouTube视频下载器

一个使用pytubefix库的YouTube视频下载器，可解决YouTube API变更导致的HTTP 410错误问题。

## 功能特点

- ✅ 修复了YouTube API变更导致的HTTP 410错误
- ✅ 支持最高质量、仅音频和最低质量三种下载模式
- ✅ 中文界面，支持中文字体显示
- ✅ 实时下载进度显示
- ✅ 视频信息获取（标题、时长、作者、观看次数）
- ✅ 自定义下载路径

## 安装说明

### 1. 确保已安装Python

程序需要Python 3.6或更高版本运行。如果您还没有安装Python，请前往 [Python官网](https://www.python.org/downloads/) 下载并安装。

### 2. 安装必要的依赖

打开命令提示符（CMD）或PowerShell，导航到程序所在目录，然后执行以下命令安装所需依赖：

```bash
# 升级pip（重要，确保能安装最新版本的库）
python -m pip install --upgrade pip

# 安装pytubefix库（解决YouTube API 410错误的关键）
python -m pip install pytubefix

# 安装其他必要依赖
python -m pip install requests
```

## 使用方法

1. 双击运行 `youtube_downloader.py` 文件启动程序
2. 在输入框中粘贴YouTube视频的URL链接
3. 点击"获取视频信息"按钮，等待程序获取视频详情
4. 选择保存路径和下载质量（最高质量、仅音频或最低质量）
5. 点击"开始下载"按钮，等待下载完成

## 常见问题解决方案

### HTTP 410错误

如果您遇到HTTP 410错误，这通常是由于YouTube API变更导致的。请执行以下命令更新pytubefix库：

```bash
python -m pip install --upgrade pytubefix
```

### 无法下载特定视频

有些视频可能受到年龄限制、区域限制或版权保护，无法通过此工具下载。对于这些视频，您可能需要手动下载或使用其他方法。

### 下载速度慢

下载速度可能受到您的网络连接、YouTube服务器响应速度以及视频质量等多种因素的影响。如果下载速度过慢，建议尝试降低下载质量。

## 文件说明

- `youtube_downloader.py` - 主程序文件，包含完整的下载功能
- `pytubefix_test.py` - 测试脚本，用于验证pytubefix库是否正常工作
- `README.md` - 程序使用说明文档

## 版本信息

当前使用的pytubefix版本：9.3.0

## 更新日志

### 最近更新
- 修复了YouTube API变更导致的HTTP 410错误
- 更新为使用pytubefix库替代原始的pytube/pytube3库
- 添加了版本检查功能，显示当前使用的pytubefix版本
- 优化了错误处理和用户界面
- 增加了URL有效性验证