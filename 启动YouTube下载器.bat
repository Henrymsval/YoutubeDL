@echo off

:: 设置控制台编码为UTF-8以支持中文
chcp 65001 > nul

:: 检查是否安装了Python
where python > nul 2>nul
if %errorlevel% neq 0 (
    echo 错误: 未找到Python安装。请先安装Python。
    echo 您可以从 https://www.python.org/downloads/ 下载Python
    pause
    exit /b 1
)

:: 检查是否安装了必要的依赖
python -c "import pytubefix" > nul 2>nul
if %errorlevel% neq 0 (
    echo 正在安装必要的依赖...
    python -m pip install --upgrade pip
    python -m pip install pytubefix requests
)

:: 启动YouTube下载器
echo 正在启动YouTube视频下载器...
python youtube_downloader.py

:: 处理退出情况
if %errorlevel% neq 0 (
    echo 程序异常退出，错误代码: %errorlevel%
    pause
)